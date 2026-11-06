import os
import subprocess

def compile_cs():
    input_cs = "src/AimAssist.cs"
    output_dll = "AimAssistAssembly.dll"
    
    print(f"[*] Đang biên dịch {input_cs}...")
    # Lệnh gọi Mono Compiler (mcs) trên Linux
    cmd = [
        "mcs", 
        "-target:library", 
        "-out:" + output_dll, 
        "-r:System.dll", 
        input_cs
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] Biên dịch thành công: {output_dll}")
    else:
        print(f"[X] Lỗi biên dịch:\n{result.stderr}")
        exit(1)

if __name__ == "__main__":
    compile_cs()
