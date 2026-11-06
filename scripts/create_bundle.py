import os
import UnityPy
from UnityPy.classes import TextAsset

# File DLL đã biên dịch (chứa code Menu)
SOURCE_DLL = "input/Assembly-CSharp-clean.bytes"
# Tên file AssetBundle đầu ra
OUTPUT_BUNDLE = "output/aimmenu_bundle"
# Tên của Asset bên trong Bundle
ASSET_NAME = "AimMenuCode"

def create_bundle():
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(SOURCE_DLL):
        print(f"[X] Không tìm thấy file DLL: {SOURCE_DLL}")
        return

    print(f"[*] Đang đọc file DLL: {SOURCE_DLL}")
    with open(SOURCE_DLL, "rb") as f:
        dll_bytes = f.read()

    print("[*] Đang tạo AssetBundle chứa DLL...")
    # Khởi tạo môi trường UnityPy
    env = UnityPy.Environment()
    
    # Tạo một TextAsset mới
    asset = TextAsset()
    asset.m_Name = ASSET_NAME
    # Chuyển byte DLL thành chuỗi (dùng surrogateescape để giữ nguyên byte)
    asset.m_Script = dll_bytes.decode("utf-8", "surrogateescape")
    
    # Thêm asset vào file
    env.file.assets.append(asset)
    
    # Lưu thành file AssetBundle
    with open(OUTPUT_BUNDLE, "wb") as f:
        f.write(env.file.save())
        
    print(f"[OK] Đã tạo AssetBundle thành công tại: {OUTPUT_BUNDLE}")

if __name__ == "__main__":
    create_bundle()
