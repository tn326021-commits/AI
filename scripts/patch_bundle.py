import UnityPy
import os

ORIGINAL_BUNDLE = "original.bundle"
MODIFIED_BUNDLE = "output/modified.bundle"
NEW_DLL_PATH = "AimAssist.dll"

def patch_bundle():
    os.makedirs("output", exist_ok=True)
    env = UnityPy.load(ORIGINAL_BUNDLE)
    
    with open(NEW_DLL_PATH, "rb") as f:
        dll_bytes = f.read()

    found = False
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            data = obj.parse_as_object()
            
            # TÌM FILE HOTFIX CỦA GAME BẠN
            # Thường là Assembly-CSharp.bytes, Hotfix.bytes, hoặc tên tương tự
            if data.m_Name in ["Assembly-CSharp", "Assembly-CSharp.bytes", "Hotfix"]:
                print(f"[*] Tìm thấy file Hotfix: {data.m_Name}, đang ghi đè...")
                
                # IFix đọc file này dưới dạng byte array
                try:
                    data.m_Script = dll_bytes.decode('utf-8', 'surrogateescape')
                except Exception as e:
                    print(f"[X] Lỗi: {e}")
                    exit(1)
                
                data.save()
                found = True
                
    if not found:
        print("[!] Không tìm thấy file Hotfix. Hãy kiểm tra tên thực tế!")
        exit(1)

    with open(MODIFIED_BUNDLE, "wb") as f:
        f.write(env.file.save())
    print(f"[OK] Đã lưu: {MODIFIED_BUNDLE}")

if __name__ == "__main__":
    patch_bundle()
