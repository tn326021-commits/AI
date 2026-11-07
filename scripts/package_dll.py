import io
import os
import sys
import UnityPy
from UnityPy.files import SerializedFile

def create_aim_drag_assetbundle(dll_path: str, output_path: str):
    try:
        # Kiểm tra file tồn tại trước khi đọc
        if not os.path.exists(dll_path):
            print(f"[-] File not found: {dll_path}", file=sys.stderr)
            print(f"[-] Working dir: {os.getcwd()}", file=sys.stderr)
            input_dir = os.path.dirname(dll_path)
            if os.path.exists(input_dir):
                print(f"[-] Files in '{input_dir}/': {os.listdir(input_dir)}", file=sys.stderr)
            else:
                print(f"[-] Folder '{input_dir}/' does not exist", file=sys.stderr)
            sys.exit(1)

        print(f"[*] Đang đọc file nhị phân từ: {dll_path}")
        with open(dll_path, "rb") as f:
            dll_bytes = f.read()
        
        # Decode mảng byte thành string với surrogateescape để giữ nguyên vẹn dữ liệu nhị phân
        script_content = dll_bytes.decode("utf-8", errors="surrogateescape")

        print("[*] Khởi tạo UnityPy Environment và SerializedFile giả lập...")
        env = UnityPy.Environment()
        
        # Sử dụng io.BytesIO(b'\x00' * 20) làm reader giả lập chạy an toàn trên Linux / GitHub Actions
        dummy_reader = io.BytesIO(b'\x00' * 20)
        
        serialized_file = SerializedFile(
            reader=dummy_reader,
            signature=0,
            version=(2022, 3, 2, 1),
            version_string="2022.3.2f1",
            big_id_enabled=0,
            target_platform=5,  # 5 tương ứng với StandaloneWindows64
            enable_type_tree=True,
            type_tree=[]
        )

        # Gắn SerializedFile vào Environment
        env.files[output_path] = serialized_file

        print("[*] Đang tạo đối tượng TextAsset (AimDragData)...")
        text_asset_data = {
            "m_Name": "AimDragData",
            "m_Script": script_content
        }
        
        # Thêm object loại TextAsset (ClassID: 49) vào SerializedFile
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
    # Đường dẫn tương đối tính từ thư mục gốc của repo
    INPUT_DLL = "input/Assembly.dll"
    OUTPUT_BUNDLE = "AimDrag.asset"

    create_aim_drag_assetbundle(INPUT_DLL, OUTPUT_BUNDLE)
