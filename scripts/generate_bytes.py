#!/usr/bin/env python3
"""
AimLock.bytes Generator - Unity Raw Binary Format
Tác giả: Zero-AI (007)
Mục đích: Tạo file .bytes nhị phân thô (Raw Binary Blob) chuẩn Unity
"""

import os
import struct
import hashlib
import zlib

OUTPUT_DIR = 'output'
FILENAME = 'AimLock.bytes'

# ============================================================
# 1. ĐÓNG GÓI DỮ LIỆU NHỊ PHÂN (STRUCT PACKING)
# ============================================================
def pack_vivo_u10():
    """Đóng gói cấu hình phần cứng Vivo U10"""
    data = b''
    # Render & Graphics (Float, Int, Byte)
    data += struct.pack('<f', 0.75)      # render_scale
    data += struct.pack('<I', 60)        # fps_limit
    data += struct.pack('<B', 0)         # shadow_quality
    data += struct.pack('<B', 0)         # anti_aliasing
    data += struct.pack('<B', 1)         # texture_quality
    data += struct.pack('<B', 0)         # particle_quality
    data += struct.pack('<B', 1)         # disable_vsync
    
    # Touch Settings
    data += struct.pack('<I', 120)       # touch_sampling
    data += struct.pack('<I', 100)       # touch_sensitivity
    data += struct.pack('<f', 0.0)       # dead_zone
    data += struct.pack('<f', 1.8)       # drag_sensitivity
    
    return data

def pack_aimlock():
    """Đóng gói cấu hình AimLock"""
    data = b''
    data += struct.pack('<f', 0.15)      # drag_threshold
    data += struct.pack('<f', 15.0)      # anti_drag_force
    data += struct.pack('<f', 0.005)     # drag_clamp
    data += struct.pack('<B', 1)         # dead_lock
    data += struct.pack('<f', 8.0)       # snap_speed
    data += struct.pack('<f', 0.0)       # lerp_factor
    data += struct.pack('<f', 3.5)       # head_scale
    data += struct.pack('<f', 0.8)       # body_scale
    data += struct.pack('<f', 0.85)      # prediction_strength
    data += struct.pack('<f', 0.85)      # recoil_compensation
    data += struct.pack('<f', 1.0)       # bullet_alignment
    data += struct.pack('<B', 1)         # ignore_body
    data += struct.pack('<B', 1)         # visible_only
    data += struct.pack('<I', 65)        # max_lock_range
    return data

def pack_bytecode():
    """Sinh mã máy (Bytecode) nhị phân thực thi logic"""
    OP_LDC_I4 = 0x20
    OP_LDC_R4 = 0x22
    OP_STIND_R4 = 0x52
    OP_MUL = 0x5A
    OP_CALL = 0x28
    OP_RET = 0x2A
    ins = []
    def emit(op, operand=0): ins.append(struct.pack('<BI', op, operand))
    
    # Logic 1: Anti-Drag (Chống kéo quá đầu)
    emit(OP_LDC_I4, 0x1000); emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 15.0))[0]); emit(OP_MUL); emit(OP_STIND_R4)
    # Logic 2: Instant Snap (Ghim đầu tức thì)
    emit(OP_LDC_I4, 0x2000); emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 8.0))[0]); emit(OP_MUL); emit(OP_CALL, 0x4000); emit(OP_RET)
    # Logic 3: Bullet Align (Căn đạn)
    emit(OP_LDC_I4, 0x3000); emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 1.0))[0]); emit(OP_MUL); emit(OP_STIND_R4)
    # Logic 4: Recoil Control (Giảm giật)
    emit(OP_LDC_I4, 0x5000); emit(OP_LDC_R4, struct.unpack('<I', struct.pack('<f', 0.85))[0]); emit(OP_MUL); emit(OP_STIND_R4)
    emit(OP_RET)
    return b''.join(ins)

# ============================================================
# 2. XUẤT FILE (.bytes)
# ============================================================
def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gộp tất cả dữ liệu nhị phân thô
    raw_payload = pack_vivo_u10() + pack_aimlock() + pack_bytecode()
    
    # Nén Zlib (để dung lượng gọn hơn nhưng vẫn là nhị phân)
    compressed = zlib.compress(raw_payload, level=9)
    
    # Header nhị phân ẩn (Chỉ là 4 byte ID và 4 byte kích thước)
    # Unity sẽ đọc từ byte thứ 8 trở đi
    header = struct.pack('<II', 0x4646414D, len(compressed)) # 'FFAM' hex
    
    # Checksum 4 bytes để verify
    checksum = struct.pack('<I', zlib.crc32(compressed) & 0xffffffff)
    
    # Ghi file (Không Base64, không JSON)
    final_data = header + compressed + checksum

    output_path = os.path.join(OUTPUT_DIR, FILENAME)
    with open(output_path, 'wb') as f:
        f.write(final_data)

    size_kb = len(final_data) / 1024
    print(f"[OK] Đã tạo: {output_path}")
    print(f"[INFO] Kích thước: {len(final_data)} bytes (~{size_kb:.2f} KB)")
    print(f"[INFO] Định dạng: Unity Raw Binary Blob (Zlib compressed)")
    print(f"[INFO] Cấu hình: Vivo U10 + AimLock")
    print(f"[INFO] 16 bytes đầu (Hex): {final_data[:16].hex()}")

if __name__ == '__main__':
    generate()
