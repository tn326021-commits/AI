import UnityPy
import os

ORIGINAL_BUNDLE = "original.bundle"
MODIFIED_BUNDLE = "output/modified.bundle"
NEW_DLL_PATH = "AimAssistAssembly.dll"

def patch_bundle():
    # Tạo thư mục output nếu chưa có
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(ORIGINAL_BUNDLE):
        print(f"[X] Không tìm thấy {ORIGINAL_BUNDLE}")
        exit(1)

    print(f"[*] Đang load bundle: {ORIGINAL_BUNDLE}")
    env = UnityPy.load(ORIGINAL_BUNDLE)
    
    with open(NEW_DLL_PATH, "rb") as f:
        new_data = f.read()

    found = False
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            data = obj.parse_as_object()
            # SỬA TÊN NÀY CHO ĐÚNG VỚI TÊN TRONG BUNDLE GỐC CỦA BẠN
            if data.m_Name in ["AimAssist", "AimAssist.bytes", "AimAssist.txt"]:
                print(f"[*] Tìm thấy: {data.m_Name}, đang ghi đè...")
                try:
                    data.m_Script = new_data.decode('utf-8')
                except UnicodeDecodeError:
                    data.m_Script = new_data.decode('utf-8', 'surrogateescape')
                data.save()
                found = True
                
    if not found:
        print("[!] Không tìm thấy slot AimAssist trong bundle. Kiểm tra lại tên!")
        exit(1)

    print(f"[*] Đang lưu file: {MODIFIED_BUNDLE}")
    with open(MODIFIED_BUNDLE, "wb") as f:
        f.write(env.file.save())
    print("[OK] Hoàn tất!")

if __name__ == "__main__":
    patch_bundle()
