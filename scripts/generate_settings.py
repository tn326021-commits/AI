#!/usr/bin/env python3
"""
Free Fire Device Optimizer - File Settings Generator
Tác giả: Zero-AI (007)
"""

import os
import json
import base64
import zlib
import hashlib
import struct

OUTPUT_DIR = 'output'
FILENAME = 'optimize.settings'

# ============================================================
# 1. CẤU HÌNH TỐI ƯU THIẾT BỊ
# ============================================================
def build_optimization_config():
    return {
        "DisplaySettings": {
            "dpi": 1200,
            "refresh_rate": 144,
            "resolution": "FHD+",
            "render_scale": 0.85,       # Giảm nhẹ để tăng FPS
            "shadow_quality": 0,        # Tắt bóng đổ
            "anti_aliasing": 0,         # Tắt khử răng cưa
            "texture_quality": 2,       # Texture cao
            "particle_quality": 0,      # Tắt hiệu ứng hạt
            "fps_limit": 144,           # Mở khóa FPS
            "disable_vsync": True       # Tắt đồng bộ dọc
        },
        "TouchSettings": {
            "touch_sensitivity": 100,   # Độ nhạy tối đa
            "touch_sampling_rate": 240, # Tần số lấy mẫu cảm ứng
            "touch_response_time": 0,   # Phản hồi tức thì
            "dead_zone": 0.01,          # Vùng chết cực nhỏ
            "drag_sensitivity": 1.5,    # Tăng lực kéo
            "precision_mode": True      # Chế độ chính xác cao
        },
        "AimOptimization": {
            "head_lock_assist": 1.0,    # Hỗ trợ khóa đầu
            "drag_to_head_ratio": 0.85, # Tỷ lệ kéo lên đầu
            "body_to_head_speed": 4.5,  # Tốc độ chuyển từ người lên đầu
            "snap_speed": 5.0,          # Tốc độ ghim cực nhanh
            "recoil_control": 0.8       # Giảm giật
        },
        "PerformanceSettings": {
            "cpu_governor": "performance",
            "gpu_governor": "performance",
            "force_gpu_rendering": True,
            "clear_cache": True,
            "kill_background_apps": True,
            "optimize_memory": True
        }
    }

# ============================================================
# 2. MÃ HÓA RỐI (OBFUSCATION)
# ============================================================
def obfuscate_data(data_bytes):
    """Mã hóa: XOR -> Zlib -> Base64 -> Đảo ngược"""
    key = b'FF_OPTIMIZE_2026_SECRET_KEY'
    
    # Bước 1: XOR
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data_bytes))
    
    # Bước 2: Nén Zlib
    compressed = zlib.compress(xored, level=9)
    
    # Bước 3: Base64 encode
    b64_encoded = base64.b64encode(compressed)
    
    # Bước 4: Đảo ngược chuỗi (tăng độ rối)
    reversed_data = b64_encoded[::-1]
    
    return reversed_data

# ============================================================
# 3. ĐÓNG GÓI FILE
# ============================================================
def generate_settings_file():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Lấy dữ liệu
    config = build_optimization_config()
    json_bytes = json.dumps(config, separators=(',', ':')).encode('utf-8')
    
    # Mã hóa rối
    obfuscated = obfuscate_data(json_bytes)
    
    # Tạo Header giả (Magic + Version + Length)
    magic = b'FFSET\x00\x01'
    version = 1
    length = len(obfuscated)
    header = struct.pack('<8sII', magic, version, length)
    
    # Checksum
    checksum = hashlib.sha256(obfuscated).digest()[:16]
    
    # Ghi file
    final_data = header + obfuscated + checksum
    output_path = os.path.join(OUTPUT_DIR, FILENAME)
    
    with open(output_path, 'wb') as f:
        f.write(final_data)
        
    print(f"[OK] Đã tạo: {output_path}")
    print(f"[INFO] Kích thước: {len(final_data)} bytes")
    print(f"[INFO] DPI: 1200 | Refresh: 144Hz | Sensitivity: 100")
    
    # Lưu file debug (JSON gốc) để đối chiếu
    debug_path = os.path.join(OUTPUT_DIR, 'settings_debug.json')
    with open(debug_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"[OK] Debug JSON: {debug_path}")

if __name__ == '__main__':
    generate_settings_file()
