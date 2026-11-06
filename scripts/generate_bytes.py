import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Cấu hình Key và IV chuẩn theo yêu cầu bảo mật AES-256
AES_KEY = b"0123456789abcdef0123456789abcdef"  # 32 bytes
AES_IV = b"abcdef0123456789"               # 16 bytes

def encrypt_file():
    source_path = "Assets/AimLock.asset"
    output_dir = "Assets/AssetBundles"
    output_path = os.path.join(output_dir, "Aimlock.asset")

    if not os.path.exists(source_path):
        print(f"[!] Không tìm thấy file nguồn tại: {source_path}")
        return

    # Đọc nội dung file asset gốc
    with open(source_path, "rb") as f:
        plain_data = f.read()

    # Thực hiện mã hoá AES-256 (CBC Mode + PKCS7 Padding)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted_data = cipher.encrypt(pad(plain_data, AES.block_size))

    # Ghi kết quả ra thư mục đích
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(encrypted_data)

    print(f"[+] Đã mã hóa thành công file asset tại: {output_path}")

if __name__ == "__main__":
    encrypt_file()
