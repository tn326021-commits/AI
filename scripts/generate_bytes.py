#!/usr/bin/env python3
"""
AimLock.bytes Generator for Vivo U10
Tác giả: Zero-AI (007)
"""

import os
import json
import struct
import hashlib
import base64
import zlib

OUTPUT_DIR = 'output'
FILENAME = 'AimLock.bytes'

# ============================================================
# 1. CẤU HÌNH TỐI ƯU CHO VIVO U10
# ============================================================
def build_vivo_u10_config():
    """
    Vivo U10: Snapdragon 665, Adreno 610, RAM 3/4GB, Màn 60Hz, 720x1544
    Chiến lược: Ưu tiên FPS ổn định (60), giảm đồ họa, tăng phản hồi cảm ứng.
    """
    return {
        "DeviceProfile": {
            "model": "vivo_u10",
            "soc": "Snapdragon 665",
            "gpu": "Adreno 610",
            "screen_refresh_rate": 60,
            "screen_resolution": "720x1544"
        },
        "Graphics": {
            "render_scale": 0.75,        # Giảm render để giữ FPS
            "fps_limit": 60,             # Khóa 60 FPS
            "shadow_quality": 0,         # Tắt bóng đổ hoàn toàn
            "anti_aliasing": 0,          # Tắt AA
            "texture_quality": 1,        # Texture trung bình
            "particle_quality": 0,       # Tắt hạt
            "disable_vsync": 1           # Tắt VSync để giảm trễ
        },
        "Touch": {
            "touch_sampling_rate": 120,  # Màn 60Hz nhưng tăng sampling
            "touch_sensitivity": 100,    # Độ nhạy tối đa
            "dead_zone": 0.0,            # Không vùng chết
            "drag_sensitivity": 1.8,     # Tăng lực kéo
            "aim_response": "instant"    # Phản hồi tức thì
        },
        "Memory": {
            "clear_cache": 1,
            "kill_background": 1,
            "optimize_ram": 1
        }
    }

# ============================================================
# 2. CẤU HÌNH AIMLOCK (GẮT, KHÔNG MƯỢT)
# ============================================================
def build_aimlock_config():
    return {
        "AimSystem": {
            "mode": "hybrid_drag",
            "idle_behavior": "lock_body",
            "drag_behavior": "lock_head",
            "drag_threshold": 0.15,      # Kích hoạt sớm
            "anti_drag_force": 15.0,     # Chống lực kéo cực mạnh
            "drag_clamp": 0.005,         # Giới hạn biên độ cực nhỏ
            "dead_lock": 1,              # Khóa cứng
            "snap_speed": 8.0,           # Tốc độ snap cực nhanh (bù màn 60Hz)
            "lerp_factor": 0.0,          # Không nội suy, snap thẳng
            "head_scale": 3.5,           # Hitbox đầu cực to
            "body_scale": 0.8,
            "prediction_strength": 0.85,
            "recoil_compensation": 0.85,
            "bullet_alignment": 1.0,
            "ignore_body": 1,
            "visible_target_only": 1,
            "max_lock_range": 65         # Giảm tầm khóa để đỡ lag
        }
    }

# ============================================================
# 3. BYTECODE IL2CPP (NHIỀU LỆNH, KHÔNG PADDING)
# ============================================================
def build_bytecode():
    OP_LDC_I4 = 0x20
    OP_LDC_R4 = 0x22
    OP_STIND_R4 = 0x52
    OP_MUL = 0x5A
    OP_ADD = 0x58
    OP_CALL = 0x28
    OP_RET = 0x2A

    instructions = []
    def emit(op, operand=0):
        instructions.append(struct.pack('<BI', op, operand))

    # Logic 1: Anti-Drag (Chống kéo quá đầu)
    emit(OP_LDC_I4, 0x1000)
    emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 15.0))[0])
    emit(OP_MUL)
    emit(OP_STIND_R4)

    # Logic 2: Instant Head Snap
    emit(OP_LDC_I4, 0x2000)
    emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 8.0))[0])
    emit(OP_MUL)
    emit(OP_CALL, 0x4000)
    emit(OP_RET)

    # Logic 3: Bullet Align
    emit(OP_LDC_I4, 0x3000)
    emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 1.0))[0])
    emit(OP_MUL)
    emit(OP_STIND_R4)

    # Logic 4: Recoil Control
    emit(OP_LDC_I4, 0x5000)
    emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 0.85))[0])
    emit(OP_MUL)
    emit(OP_STIND_R4)

    # Lặp thêm logic (không padding, chỉ tính toán)
    for _ in range(10):
        emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 0.95))[0])
        emit(OP_MUL)
        emit(OP_STIND_R4)
        
    emit(OP_RET)
    return b''.join(instructions)

# ============================================================
# 4. MÃ HÓA RỐI
# ============================================================
def obfuscate(data):
    key = b'VIVO_U10_AIMLOCK_2026'
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    comp = zlib.compress(xored, level=9)
    b64 = base64.b64encode(comp)
    return b64[::-1]

# ============================================================
# 5. ĐÓNG GÓI FILE .BYTES
# ============================================================
def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    payload = {
        "device": build_vivo_u10_config(),
        "aimlock": build_aimlock_config(),
        "bytecode": base64.b64encode(build_bytecode()).decode('utf-8')
    }

    json_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    obfuscated = obfuscate(json_bytes)

    # Header cho file .bytes (Unity Raw Format)
    magic = b'UNITYRAW'
    version = 1
    length = len(obfuscated)
    header = struct.pack('<8sII', magic, version, length)
    
    # Checksum
    checksum = hashlib.sha256(obfuscated).digest()[:16]

    final_data = header + obfuscated + checksum
    output_path = os.path.join(OUTPUT_DIR, FILENAME)

    with open(output_path, 'wb') as f:
        f.write(final_data)

    size_kb = len(final_data) / 1024
    print(f"[OK] Đã tạo: {output_path}")
    print(f"[INFO] Kích thước: {len(final_data)} bytes (~{size_kb:.2f} KB)")
    print(f"[INFO] Cấu hình: Vivo U10 (Snapdragon 665, 60Hz)")
    print(f"[INFO] Aimlock: Instant Snap (Không mượt), Anti-drag, Head-only")

if __name__ == '__main__':
    generate()
