import os

ORIGINAL_BYTES = "input/Assembly-CSharp-patch.bytes"
NEW_DLL = "AimAssistAssembly.dll"
OUTPUT_BYTES = "output/Assembly-CSharp-patch.bytes"

def create_ifix_patch():
    os.makedirs("output", exist_ok=True)
    
    print(f"[*] Đang đọc file gốc: {ORIGINAL_BYTES}")
    with open(ORIGINAL_BYTES, "rb") as f:
        original_data = f.read()

    # Tìm vị trí kết thúc của phần Header (thường là nơi bắt đầu mã IL)
    # Chúng ta tìm chuỗi ký tự đánh dấu kết thúc danh sách tham chiếu (ví dụ: null byte hoặc một mẫu cụ thể)
    # Ở đây, tôi sẽ lấy 2000 byte đầu tiên làm Header mẫu (bạn có thể điều chỉnh con số này)
    header_size = 2000
    header_data = original_data[:header_size]

    print(f"[*] Đang đọc code Menu: {NEW_DLL}")
    with open(NEW_DLL, "rb") as f:
        new_code = f.read()

    print("[*] Đang ghép Header + Code Menu...")
    with open(OUTPUT_BYTES, "wb") as f:
        f.write(header_data)
        f.write(new_code)

    print(f"[OK] Đã tạo file IFix Patch tại: {OUTPUT_BYTES}")

if __name__ == "__main__":
    create_ifix_patch()
