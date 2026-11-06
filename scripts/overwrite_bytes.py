import os

# File DLL chứa Menu của bạn (được sinh ra từ bước Compile)
NEW_DLL = "AimAssistAssembly.dll"
# File kết quả
OUTPUT_BYTES = "output/Assembly-CSharp-clean.bytes"

def overwrite_bytes():
    # Tạo thư mục output nếu chưa có
    os.makedirs("output", exist_ok=True)
    
    print(f"[*] Đang đọc file DLL Menu mới: {NEW_DLL}")
    if not os.path.exists(NEW_DLL):
        print(f"[X] Lỗi: Không tìm thấy {NEW_DLL}")
        return

    # Đọc toàn bộ dữ liệu của file DLL
    with open(NEW_DLL, "rb") as f:
        new_data = f.read()

    print("[*] Đang xóa nội dung cũ và tạo file .bytes mới...")
    # GHI ĐÈ: Tạo ra file .bytes hoàn toàn mới
    with open(OUTPUT_BYTES, "wb") as f:
        f.write(new_data)
        
    print(f"[OK] Đã tạo file thành công! File lưu tại: {OUTPUT_BYTES}")

if __name__ == "__main__":
    overwrite_bytes()
