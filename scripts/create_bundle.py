import os
import UnityPy
from UnityPy.classes import TextAsset

# Đường dẫn file
TEMPLATE_BUNDLE = "input/aimmenu_bundle_empty" # Bạn cần có 1 file bundle trống ở đây
SOURCE_DLL = "input/Assembly-CSharp-clean.bytes"
OUTPUT_BUNDLE = "output/aimmenu_bundle" # Tên file đầu ra
ASSET_NAME = "AimMenuCode"

def create_bundle():
    os.makedirs("output", exist_ok=True)
    
    # Nếu không có file bundle trống, ta tạo một file rỗng giả lập để test
    if not os.path.exists(TEMPLATE_BUNDLE):
        print(f"[!] Không tìm thấy file mẫu {TEMPLATE_BUNDLE}. Tạo file rỗng...")
        with open(TEMPLATE_BUNDLE, "wb") as f:
            f.write(b"UnityFS\x00") # Header giả lập

    print(f"[*] Đang đọc file DLL: {SOURCE_DLL}")
    with open(SOURCE_DLL, "rb") as f:
        dll_bytes = f.read()

    print("[*] Đang tạo AssetBundle chứa DLL...")
    try:
        # Load bundle trống
        env = UnityPy.load(TEMPLATE_BUNDLE)
        
        # Tạo TextAsset
        asset = TextAsset(m_Name=ASSET_NAME, m_Script=dll_bytes.decode("utf-8", "surrogateescape"))
        
        # Nhét asset vào file đầu tiên
        if env.files:
            for file_obj in env.files.values():
                file_obj.assets.append(asset)
                break
        else:
            print("[X] File bundle mẫu không hợp lệ (không có file object).")
            return

        # Lưu ra file (Dùng hàm save() của file object)
        with open(OUTPUT_BUNDLE, "wb") as f:
            f.write(env.file.save()) # Lưu ý: env.file là thuộc tính, không phải hàm
            
        print(f"[OK] Đã tạo AssetBundle thành công tại: {OUTPUT_BUNDLE}")

    except Exception as e:
        print(f"[X] Lỗi khi tạo bundle: {e}")

if __name__ == "__main__":
    create_bundle()
