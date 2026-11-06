import os

ORIGINAL_BYTES = "đầu vào/Assembly-CSharp-patch.bytes" # File bạn đã up lên
OUTPUT_BYTES = "đầu ra/Assembly-CSharp-hitbox_x3.bytes"
COMPILED_DLL = "AimAssistAssembly.dll" # File sinh ra từ bước biên dịch C#

def patch_bytes():
    os.makedirs("đầu ra", exist_ok=True)
    
    if not os.path.exists(COMPILED_DLL):
        print(f"[X] Không tìm thấy file {COMPILED_DLL}. Hãy kiểm tra bước biên dịch!")
        return

    print("[*] Đang đọc file patch gốc...")
    # Không cần đọc file gốc nếu ta muốn xóa sạch, nhưng ta cần tạo thư mục
    # Chúng ta sẽ ghi đè hoàn toàn bằng file DLL mới tinh
    
    with open(COMPILED_DLL, "rb") as f:
        new_data = f.read()

    # GHI ĐÈ: Tạo file bytes mới hoàn toàn từ DLL đã biên dịch
    with open(OUTPUT_BYTES, "wb") as f:
        f.write(new_data)
    
    print(f"[OK] Đã xóa nội dung cũ và tạo file Hitbox x3 thành công: {OUTPUT_BYTES}")

if __name__ == "__main__":
    patch_bytes()
