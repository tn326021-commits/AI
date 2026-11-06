import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Cấu hình Key và IV chuẩn theo yêu cầu bảo mật AES-256
AES_KEY = b"0123456789abcdef0123456789abcdef"  # 32 bytes
AES_IV = b"abcdef0123456789"               # 16 bytes

def generate_and_encrypt():
    asset_dir = "Assets"
    output_dir = "Assets/AssetBundles"
    source_path = os.path.join(asset_dir, "AimLock.asset")
    output_path = os.path.join(output_dir, "Aimlock.asset")

    os.makedirs(asset_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    yaml_content = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!114 &11400000
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: 0}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {fileID: 11500000, guid: 0000000000000000e000000000000000, type: 3}
  m_Name: AimLock
  headBoneName: "Bip01_Head"
  maxDistance: 120.0
  viewAngle: 25.0
  headOffset:
    x: 0.0
    y: 0.08
    z: 0.02
  targetPredictionMultiplier: 0.75
  smoothingSpeed: 25.0
  requireLineOfSight: 1
  prioritizeCenterScreen: 1
"""

    with open(source_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    with open(source_path, "rb") as f:
        plain_data = f.read()

    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted_data = cipher.encrypt(pad(plain_data, AES.block_size))

    with open(output_path, "wb") as f:
        f.write(encrypted_data)
    
    print(f"[+] Đã tạo và mã hóa thành công file tại: {output_path}")

if __name__ == "__main__":
    generate_and_encrypt()
