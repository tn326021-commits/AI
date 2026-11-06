import os
import UnityPy
from UnityPy.classes import TextAsset

# Sử dụng file original.bundle của bạn làm khuôn mẫu
TEMPLATE_BUNDLE = "đầu vào/original.bundle" 
# File DLL chứa code Menu
SOURCE_DLL = "đầu vào/Assembly-CSharp-clean.bytes"
# File AssetBundle đầu ra
OUTPUT_BUNDLE = "đầu ra/aimmenu_bundle"
# Tên của Asset bên trong
ASSET_NAME = "AimMenuCode"

def create_bundle():
    # Tạo thư mục đầu ra nếu chưa có
    os.makedirs("đầu ra", exist_ok=True)
    
    if not os.path.exists(TEMPLATE_BUNDLE):
        print(f"[X] Không tìm thấy file mẫu: {TEMPLATE_BUNDLE}")
        return

    if not os.path.exists(SOURCE_DLL):
        print(f"[X] Không tìm thấy file DLL: {SOURCE_DLL}")
        return

    print(f"[*] Đang đọc file DLL: {SOURCE_DLL}")
    with open(SOURCE_DLL, "rb") as f:
        dll_bytes = f.read()

    print("[*] Đang tạo AssetBundle chứa DLL...")
    try:
        # Mở file bundle gốc của bạn
        env = UnityPy.load(TEMPLATE_BUNDLE)
        
        # Tạo TextAsset chứa code
        asset = TextAsset(m_Name=ASSET_NAME, m_Script=dll_bytes.decode("utf-8", "surrogateescape"))
        
        # Thêm vào file đầu tiên trong bundle
        if env.files:
            for file_obj in env.files.values():
                file_obj.assets.append(asset)
                break
        else:
            print("[X] File bundle mẫu không hợp lệ.")
            return

        # Lưu ra file mới
        with open(OUTPUT_BUNDLE, "wb") as f:
            f.write(env.file.save())
            
        print(f"[OK] Đã tạo AssetBundle thành công tại: {OUTPUT_BUNDLE}")

    except Exception as e:
        print(f"[X] Lỗi khi tạo bundle: {e}")

if __name__ == "__main__":
    create_bundle()
