import os
import UnityPy
import clr

# Tải dnlib (nếu chưa có)
DNLIB_PATH = "dnlib.dll"
if os.path.exists(DNLIB_PATH):
    clr.AddReference(os.path.abspath(DNLIB_PATH))

from dnlib.DotNet import ModuleDefMD, ModuleWriterOptions
from dnlib.DotNet.Writer import MetadataFlags

ORIGINAL_BYTES = "input/Assembly-CSharp-patch.bytes"
NEW_DLL = "AimAssistAssembly.dll"
OUTPUT_BYTES = "output/Assembly-CSharp-menu.bytes"

def patch_bytes():
    os.makedirs("output", exist_ok=True)
    
    print("[*] Load original .bytes file...")
    main_module = ModuleDefMD.Load(ORIGINAL_BYTES)
    
    print("[*] Removing old classes...")
    types_to_remove = [t for t in main_module.Types if t.Name != "<Module>"]
    for t in types_to_remove:
        main_module.Types.Remove(t)
        
    print("[*] Loading new DLL...")
    new_module = ModuleDefMD.Load(NEW_DLL)
    
    print("[*] Injecting new classes...")
    for t in new_module.Types:
        if t.Name == "<Module>": continue
        main_module.Types.Add(t)
        
    print("[*] Saving new .bytes...")
    options = ModuleWriterOptions(main_module)
    options.MetadataOptions.Flags |= MetadataFlags.PreserveAll
    main_module.Write(OUTPUT_BYTES, options)
    
    print(f"[OK] Done! File saved: {OUTPUT_BYTES}")

if __name__ == "__main__":
    patch_bytes()
