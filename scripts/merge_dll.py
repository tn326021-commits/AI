import os
import clr

# Tải dnlib từ NuGet
DNLIB_PATH = "dnlib.dll" 
if not os.path.exists(DNLIB_PATH):
    os.system("wget https://github.com/0xd4d/dnlib/releases/download/v4.3.0/dnlib.dll")

clr.AddReference(os.path.abspath(DNLIB_PATH))

from dnlib.DotNet import ModuleDefMD, ModuleDef, ModuleWriterOptions
from dnlib.DotNet.Writer import MetadataOptions, MetadataFlags

PATCH_BYTES = "đầu vào/Assembly-CSharp-patch.bytes"
NEW_DLL = "AimAssistAssembly.dll"
OUTPUT = "đầu ra/Assembly-CSharp-merged.bytes"

def merge():
    os.makedirs("đầu ra", exist_ok=True)
    
    print("[*] Đang mở file patch gốc...")
    # File patch thực chất là DLL, load nó
    main_module = ModuleDefMD.Load(PATCH_BYTES)
    
    print("[*] Đang mở DLL mới...")
    new_module = ModuleDefMD.Load(NEW_DLL)
    
    print("[*] Đang gộp class...")
    for type_def in new_module.Types:
        if type_def.Name == "<Module>": continue
        # Thêm class mới vào file patch
        main_module.Types.Add(type_def)
    
    print("[*] Đang lưu file mới...")
    options = ModuleWriterOptions(main_module)
    options.MetadataOptions.Flags |= MetadataFlags.PreserveAll
    main_module.Write(OUTPUT, options)
    
    print(f"[OK] Đã tạo file: {OUTPUT}")

if __name__ == "__main__":
    merge()
