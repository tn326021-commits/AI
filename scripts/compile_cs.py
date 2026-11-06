import os
import clr
import subprocess

def setup_roslyn():
    # Tải thư viện Roslyn từ NuGet (có sẵn trên GitHub Actions)
    subprocess.run(["dotnet", "new", "console", "-n", "TempConsole", "-o", "temp_roslyn"], check=True)
    subprocess.run(["dotnet", "add", "temp_roslyn/TempConsole.csproj", "package", "Microsoft.CodeAnalysis.CSharp"], check=True)
    
    # Đường dẫn tới Roslyn DLL trong NuGet cache
    nuget_path = os.path.expanduser("~/.nuget/packages/microsoft.codeanalysis.csharp/4.8.0/lib/netstandard2.0/")
    roslyn_common = os.path.expanduser("~/.nuget/packages/microsoft.codeanalysis.common/4.8.0/lib/netstandard2.0/")
    
    clr.AddReference(os.path.join(roslyn_common, "Microsoft.CodeAnalysis.dll"))
    clr.AddReference(os.path.join(nuget_path, "Microsoft.CodeAnalysis.CSharp.dll"))

def compile_ifix_script(input_cs, output_dll, unity_dll_dir):
    from Microsoft.CodeAnalysis import MetadataReference
    from Microsoft.CodeAnalysis.CSharp import CSharpCompilation, CSharpSyntaxTree, CSharpCompilationOptions, OutputKind
    from System.Collections.Generic import List

    print(f"[*] Đang biên dịch IFix script: {input_cs}")
    with open(input_cs, "r", encoding="utf-8") as f:
        source = f.read()

    syntax_tree = CSharpSyntaxTree.ParseText(source)
    
    # Tham chiếu các thư viện quan trọng từ danh sách của bạn
    references = List[MetadataReference]()
    ref_dlls = [
        "mscorlib.dll", "System.dll", "System.Core.dll", 
        "UnityEngine.dll", "UnityEngine.CoreModule.dll", 
        "UnityEngine.PhysicsModule.dll", "UnityEngine.AnimationModule.dll",
        "IFix.Core.dll", "Assembly-CSharp.dll"
    ]
    
    for dll in ref_dlls:
        path = os.path.join(unity_dll_dir, dll)
        if os.path.exists(path):
            references.Add(MetadataReference.CreateFromFile(path))
        else:
            print(f"[!] Không tìm thấy: {dll}")

    compilation = CSharpCompilation.Create(
        "AimAssistHotfix", # Tên Assembly của bạn
        [syntax_tree],
        references,
        CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary)
    )

    emit_result = compilation.Emit(output_dll)
    if emit_result.Success:
        print(f"[OK] Biên dịch IFix DLL thành công: {output_dll}")
    else:
        print("[X] Lỗi biên dịch:")
        for diag in emit_result.Diagnostics:
            if diag.Severity == 1:
                print(diag.ToString())
        exit(1)

if __name__ == "__main__":
    setup_roslyn()
    # unity_dll_dir là nơi chứa các file DLL bạn đã liệt kê (bạn cần upload chúng lên repo)
    compile_ifix_script("src/AimAssist.cs", "AimAssist.dll", "libs/")
