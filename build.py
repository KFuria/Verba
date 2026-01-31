import subprocess
import sys
from pathlib import Path
import PyInstaller

def main() -> None:
    """Build the app executable using PyInstaller."""
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    main_file = src_dir / "main.py"
    icon_file = project_root / "icon.ico"
    
      
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Single executable
        "--windowed",          # No console window
        "--name", "Verba",
        "--distpath", str(project_root / "dist"),
        "--workpath", str(project_root / "build"),
        "--specpath", str(project_root),
        "--icon", str(icon_file),
        "--add-data", f"{icon_file};.",
        # Add src directory to path so imports work
        "--paths", str(src_dir),
        # Clean build
        "--clean",
        # Main entry point
        str(main_file),
    ]
    
    print("\nBuilding executable...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(project_root))
    
    if result.returncode == 0:
        exe_path = project_root / "dist" / "Verba.exe"
        print("\n" + "=" * 50)
        print("BUILD SUCCESSFUL!")
        print("=" * 50)
        print(f"\nExecutable created at:\n  {exe_path}")
        print("\nNote: The 'data' folder will be created next to the")
        print("executable when you first run it.")
    else:
        print("\n" + "=" * 50)
        print("BUILD FAILED!")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
