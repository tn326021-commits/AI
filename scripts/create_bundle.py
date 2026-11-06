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
    
    # Tạo một Environment trống
    env = UnityPy.Environment()
    
    # Tạo TextAsset bằng cách truyền tham số trực tiếp
    asset = TextAsset(m_Name=ASSET_NAME, m_Script=dll_bytes)
    
    # SỬA LỖI: Thay 'env.file' bằng 'env.files' để phù hợp với API mới
    # Tạo một SerializedFile mới để chứa asset
    from UnityPy.files import SerializedFile
    new_file = SerializedFile()
    new_file.assets.append(asset)
    env.files["aimmenu"] = new_file
    
    # Lưu thành file AssetBundle
    # Sử dụng trực tiếp đối tượng file vừa tạo để lưu
    with open(OUTPUT_BUNDLE, "wb") as f:
        f.write(new_file.save())
        
    print(f"[OK] Đã tạo AssetBundle thành công tại: {OUTPUT_BUNDLE}")

if __name__ == "__main__":
    create_bundle()
