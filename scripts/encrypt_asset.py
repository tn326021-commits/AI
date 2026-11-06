import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Cấu hình chuẩn theo yêu cầu bảo mật AES-256
AES_KEY = b"0123456789abcdef0123456789abcdef"  # 32 bytes
AES_IV = b"abcdef0123456789"               # 16 bytes

def generate_and_encrypt_ultimate():
    # 1. Khai báo các đường dẫn thư mục
    asset_dir = "Assets"
    output_dir = "Assets/AssetBundles"
    source_path = os.path.join(asset_dir, "AimLock.asset")
    output_path = os.path.join(output_dir, "Aimlock.asset")

    # Đảm bảo thư mục tồn tại trên môi trường Linux của GitHub Actions
    os.makedirs(asset_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 2. Nội dung YAML cấu hình AimLockHead Ultimate đầy đủ và chi tiết nhất
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
  
  # ==========================================
  # AIMLOCKHEAD ULTIMATE CONFIGURATION
  # ==========================================
  headBoneNames:
    - "Head"
    - "Bip01_Head"
    - "Neck"
  autoDetectBoneInChildren: 1
  allowBodyFallbackIfHeadMissing: 1

  # Khoảng cách & Góc nhìn FOV
  minTargetDistance: 1.0
  maxLockDistance: 200.0
  lockFieldOfView: 18.0
  innerDeadZoneRadius: 1.5

  # Bù trừ đạn đạo & Dự đoán chuyển động
  headOffsetAdjustment:
    x: 0.0
    y: 0.07
    z: 0.01
  enableBallisticPrediction: 1
  projectileSpeed: 500.0
  gravityCorrectionFactor: 0.4
  maxPredictionTimeStep: 0.5

  # Tốc độ & Độ mượt (Smoothing)
  smoothingAlgorithmType: 2
  smoothDampTime: 0.05
  maxRotationSpeed: 450.0
  snapToTargetThreshold: 0.02

  # Bộ lọc môi trường & Vật cản
  strictLineOfSight: 1
  raycastCheckFrequency: 0.05
  obstructionLayers:
    serializedVersion: 2
    m_Bits: 4294967295
  ignoreTransparentObjects: 1

  # Thuật toán ưu tiên mục tiêu
  prioritizeCenterScreen: 1
  prioritizeLowestHealth: 0
  switchTargetCooldownDuration: 0.1
  stickyTargetLock: 1

  # Giao diện & Hiệu ứng
  enableHeadshotCrosshairUI: 1
  crosshairHighlightScale: 1.35
  lockOnIndicatorColor:
    r: 1.0
    v: 0.0
    b: 0.0
    a: 1.0
"""

    # 3. Ghi file YAML nguồn
    with open(source_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print(f"[+] Đã tự động sinh file cấu hình YAML tại: {source_path}")

    # 4. Đọc dữ liệu và mã hóa AES-256 (CBC Mode + PKCS7 Padding)
    with open(source_path, "rb") as f:
        plain_data = f.read()

    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted_data = cipher.encrypt(pad(plain_data, AES.block_size))

    # 5. Ghi file mã hóa đầu ra
    with open(output_path, "wb") as f:
        f.write(encrypted_data)
    
    print(f"[+] Đã mã hóa thành công file Aimlock.asset tại: {output_path}")

if __name__ == "__main__":
    generate_and_encrypt_ultimate()
