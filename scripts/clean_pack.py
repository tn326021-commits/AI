import os

ORIGINAL_BYTES = "input/Assembly-CSharp-patch.bytes"
NEW_DLL = "AimAssistAssembly.dll"
OUTPUT = "output/Assembly-CSharp-clean.bytes"

def clean_and_pack():
    os.makedirs("output", exist_ok=True)
    
    print(f"[*] Đang xóa nội dung file cũ...")
    # Ghi đè một file rỗng (hoặc bỏ qua hoàn toàn file gốc)
    # Ở đây chúng ta tạo file mới hoàn toàn từ DLL
    
    print(f"[*] Đang nạp code mới từ: {NEW_DLL}")
    with open(NEW_DLL, "rb") as f:
        new_data = f.read()

    with open(OUTPUT, "wb") as f:
        f.write(new_data)
        
    print(f"[OK] Đã tạo file thành công (Chỉ chứa code mới): {OUTPUT}")

if __name__ == "__main__":
    clean_and_pack()
