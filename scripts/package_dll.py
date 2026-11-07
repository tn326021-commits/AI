import io
import sys
import os
import UnityPy
from UnityPy.files import SerializedFile

def create_aim_drag_assetbundle(dll_path: str, output_path: str):
    try:
        # Tự động lấy đường dẫn tuyệt đối dựa trên vị trí file script hiện tại
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Nếu script nằm trong thư mục scripts/, ta lùi về thư mục gốc 1 cấp để tìm thư mục AI/input/
        # Hoặc nếu script nằm ở thư mục gốc, chỉnh lại cho phù hợp. Dưới đây là cách an toàn nhất:
        absolute_dll_path = os.path.normpath(os.path.join(base_dir, "..", dll_path))
        
        print(f"[*] Đang tìm file tại: {absolute_dll_path}")
        with open(absolute_dll_path, "rb") as f:
            dll_bytes = f.read()
        
        script_content = dll_bytes.decode("utf-8", errors="surrogateescape")

        print("[*] Khởi tạo UnityPy Environment và SerializedFile giả lập...")
        env = UnityPy.Environment()
        
        dummy_reader = io.BytesIO(b'\x00' * 20)
        
        serialized_file = SerializedFile(
            reader=dummy_reader,
            signature=0,
            version=(2022, 3, 2, 1),
            version_string="2022.3.2f1",
            big_id_enabled=0,
            target_platform=5,
            enable_type_tree=True,
            type_tree=[]
        )

        env.files[output_path] = serialized_file

        print("[*] Đang tạo đối tượng TextAsset (AimDragData)...")
        text_asset_data = {
            "m_Name": "AimDragData",
            "m_Script": script_content
        }
        
        serialized_file.create_object(
            class_id=49,
            container=text_asset_data
        )

        print(f"[*] Đang ghi file AssetBundle ra: {output_path}")
        bundle_data = env.save(packer="none")
        
        with open(output_path, "wb") as out_f:
            out_f.write(bundle_data)
            
        print(f"[+] Đã đóng gói thành công file AssetBundle tại: {output_path}")

    except Exception as e:
        print("[-] Đã xảy ra lỗi trong quá trình đóng gói AssetBundle:", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Đường dẫn tương đối từ thư mục gốc của repo
    INPUT_DLL = "AI/input/Assembly.dll"        
    OUTPUT_BUNDLE = "AimDrag.asset" 
    
    create_aim_drag_assetbundle(INPUT_DLL, OUTPUT_BUNDLE)
