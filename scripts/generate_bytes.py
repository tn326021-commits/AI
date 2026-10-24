#!/usr/bin/env python3
"""
AimLock.bytes Generator - Unity TextAsset Format (Raw JSON)
Tác giả: Zero-AI (007)
"""

import os
import json

OUTPUT_DIR = 'output'
FILENAME = 'AimLock.bytes'

# ============================================================
# 1. CẤU HÌNH TỐI ƯU VIVO U10
# ============================================================
def build_config():
    return {
        "DeviceProfile": {
            "model": "vivo_u10",
            "soc": "Snapdragon 665",
            "gpu": "Adreno 610",
            "screen_refresh_rate": 60,
            "resolution": "720x1544"
        },
        "GraphicsSettings": {
            "render_scale": 0.75,
            "fps_limit": 60,
            "shadow_quality": 0,
            "anti_aliasing": 0,
            "texture_quality": 1,
            "particle_quality": 0,
            "disable_vsync": True
        },
        "TouchSettings": {
            "touch_sampling_rate": 120,
            "touch_sensitivity": 100,
            "dead_zone": 0.0,
            "drag_sensitivity": 1.8,
            "aim_response": "instant"
        },
        "AimLock": {
            "mode": "hybrid_drag",
            "idle_behavior": "lock_body",
            "drag_behavior": "lock_head",
            "drag_threshold": 0.15,
            "anti_drag_force": 15.0,
            "drag_clamp": 0.005,
            "dead_lock": True,
            "snap_speed": 8.0,
            "lerp_factor": 0.0,
            "head_scale": 3.5,
            "body_scale": 0.8,
            "prediction_strength": 0.85,
            "recoil_compensation": 0.85,
            "bullet_alignment": 1.0,
            "ignore_body": True,
            "visible_target_only": True,
            "max_lock_range": 65
        },
        "MemoryOptimization": {
            "clear_cache": True,
            "kill_background_apps": True,
            "optimize_ram": True
        }
    }

# ============================================================
# 2. GHI FILE .BYTES (RAW JSON - UNITY TEXTASSET)
# ============================================================
def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    config = build_config()
    
    # Chuyển sang JSON string (UTF-8) - Đây là nội dung file .bytes
    json_str = json.dumps(config, indent=2, ensure_ascii=False)
    raw_bytes = json_str.encode('utf-8')

    output_path = os.path.join(OUTPUT_DIR, FILENAME)
    with open(output_path, 'wb') as f:
        f.write(raw_bytes)

    size_kb = len(raw_bytes) / 1024
    print(f"[OK] Đã tạo: {output_path}")
    print(f"[INFO] Kích thước: {len(raw_bytes)} bytes (~{size_kb:.2f} KB)")
    print(f"[INFO] Định dạng: Unity TextAsset (JSON thuần, không mã hóa)")
    print(f"[INFO] Tối ưu cho: Vivo U10 (Snapdragon 665, 60Hz)")
    print(f"[INFO] AimLock: Kéo tâm -> Ghim đầu, Không kéo -> Ghim người")

if __name__ == '__main__':
    generate()
