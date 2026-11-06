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
    # (Sửa lỗi: TextAsset cần m_Name và m_Script khi khởi tạo)
    asset = TextAsset(m_Name=ASSET_NAME, m_Script=dll_bytes)
    
    # Thêm asset vào file (tạo một SerializedFile mới)
    env.file.assets.append(asset)
    
    # Lưu thành file AssetBundle
    with open(OUTPUT_BUNDLE, "wb") as f:
        f.write(env.file.save())
        
    print(f"[OK] Đã tạo AssetBundle thành công tại: {OUTPUT_BUNDLE}")

if __name__ == "__main__":
    create_bundle()
