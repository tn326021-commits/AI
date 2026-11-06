import os

ORIGINAL_BYTES = "input/Assembly-CSharp-patch.bytes" # File gốc bạn tải lên
NEW_CS_CODE = "src/AimAssist.cs" # Code menu mới của bạn
OUTPUT_BYTES = "output/Assembly-CSharp-patch.bytes"

def patch_bytes():
    os.makedirs("output", exist_ok=True)
    
    print(f"[*] Đang đọc code Menu mới từ: {NEW_CS_CODE}")
    if not os.path.exists(NEW_CS_CODE):
        print("[X] Không tìm thấy code Menu.")
        return
        
    with open(NEW_CS_CODE, "r", encoding="utf-8") as f:
        new_code = f.read()

    # Tạo một Header giả lập của IFix (thường IFix bắt đầu bằng chữ ký đặc biệt)
    # Nếu file gốc của bạn có chữ ký này, ta sẽ giữ lại nó.
    
    if os.path.exists(ORIGINAL_BYTES):
        print(f"[*] Đang mở file patch cũ để lấy cấu trúc...")
        with open(ORIGINAL_BYTES, "rb") as f:
            original_data = f.read()
            
        # Tìm điểm bắt đầu của mã code cũ (thường là text)
        # Tạm thời chúng ta sẽ nối code mới vào cuối file gốc
        # IFix sẽ quét file và biên dịch tất cả class nó tìm thấy.
        
        # Mẹo: Chúng ta ghi đè file output bằng code mới hoàn toàn, 
        # nhưng giữ lại 100 byte đầu tiên của file gốc (để giữ chữ ký IFix).
        signature = original_data[:100] if len(original_data) > 100 else b""
        
        with open(OUTPUT_BYTES, "wb") as f:
            f.write(signature) # Ghi chữ ký IFix
            f.write(new_code.encode("utf-8")) # Ghi code mới (Menu)
            
        print(f"[OK] Đã thay thế code cũ bằng Menu mới! File lưu tại: {OUTPUT_BYTES}")
    else:
        print("[X] Không tìm thấy file patch gốc trong thư mục input/")
        # Nếu không có file gốc, chỉ tạo file code thuần
        with open(OUTPUT_BYTES, "w", encoding="utf-8") as f:
            f.write(new_code)

if __name__ == "__main__":
    patch_bytes()
