import os
import UnityPy
from UnityPy.classes import TextAsset

# File bundle trống (khuôn mẫu)
TEMPLATE_BUNDLE = "input/aimmenu_bundle_empty"
# File DLL đã biên dịch
SOURCE_DLL = "input/Assembly-CSharp-clean.bytes"
# File đầu ra
OUTPUT_BUNDLE = "output/aimmenu_bundle"
ASSET_NAME = "AimMenuCode"

def create_bundle():
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(TEMPLATE_BUNDLE):
        print(f"[X] Không tìm thấy file bundle trống: {TEMPLATE_BUNDLE}")
        return

    # Đọc dữ liệu DLL
    with open(SOURCE_DLL, "rb") as f:
        dll_bytes = f.read()

    print("[*] Đang tải bundle trống...")
    env = UnityPy.load(TEMPLATE_BUNDLE)
    
    # Tạo TextAsset mới
    print("[*] Đang thêm TextAsset vào bundle...")
    asset = TextAsset(m_Name=ASSET_NAME, m_Script=dll_bytes.decode("utf-8", "surrogateescape"))
    
    # Thêm asset vào file đầu tiên trong bundle
    for file_obj in env.files.values():
        file_obj.assets.append(asset)
        break
    
    # Lưu bundle
    with open(OUTPUT_BUNDLE, "wb") as f:
        f.write(env.file.save())
    
    print(f"[OK] Đã tạo AssetBundle: {OUTPUT_BUNDLE}")

if __name__ == "__main__":
    create_bundle()
