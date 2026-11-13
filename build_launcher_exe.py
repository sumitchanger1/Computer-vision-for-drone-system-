"""
Build EXE for Desktop AI Assistant
Save as: build_exe.py in C:\Users\Admin\desktop-ai-assistant\
Run: python build_exe.py
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

def print_banner(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_file_exists(filepath):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"  ✅ Found: {filepath}")
        return True
    else:
        print(f"  ❌ Missing: {filepath}")
        return False

def verify_project_files():
    """Verify all required files exist"""
    print_banner("📋 VERIFYING PROJECT FILES")
    
    required_files = [
        "launcher.py",
        "ai_pattern_recognition.py",
        "automation_engine.py",
        "data_manager.py",
        "pattern_recognition.py",
        "video_processor.py",
        "workflow_builder.py",
    ]
    
    all_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_exist = False
    
    # Check data folder
    if os.path.exists("data"):
        print(f"  ✅ Found: data/ folder")
    else:
        print(f"  ⚠️  Warning: data/ folder not found (will be created at runtime)")
    
    return all_exist

def install_pyinstaller():
    """Install PyInstaller"""
    print_banner("📦 CHECKING PYINSTALLER")
    
    try:
        import PyInstaller
        print("  ✅ PyInstaller already installed")
        return True
    except ImportError:
        print("  📥 Installing PyInstaller...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✅ PyInstaller installed successfully")
            return True
        else:
            print("  ❌ Failed to install PyInstaller")
            print(result.stderr)
            return False

def clean_build():
    """Clean previous build files"""
    print_banner("🧹 CLEANING OLD BUILD FILES")
    
    folders = ["build", "dist", "__pycache__"]
    for folder in folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  ✅ Removed: {folder}/")
            except Exception as e:
                print(f"  ⚠️  Could not remove {folder}: {e}")
    
    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"  ✅ Removed: {spec_file}")
        except Exception as e:
            print(f"  ⚠️  Could not remove {spec_file}: {e}")

def build_exe():
    """Build the EXE using PyInstaller"""
    print_banner("🔨 BUILDING EXE")
    
    # All Python modules to include
    hidden_imports = [
        # Video/Image processing
        "cv2",
        "numpy",
        "PIL",
        "mss",
        
        # Audio processing
        "sounddevice",
        "vosk",
        "wave",
        "pyaudio",
        "scipy",
        "scipy.fft",
        
        # Automation
        "pyautogui",
        "pynput",
        "keyboard",
        "mouse",
        "screeninfo",
        
        # Networking/AI
        "requests",
        "json",
        
        # System
        "pathlib",
        "datetime",
        "threading",
        "queue",
    ]
    
    print("\n  Building with PyInstaller...")
    print(f"  Main script: launcher.py")
    print(f"  Output name: DesktopAIAssistant.exe\n")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single EXE
        "--name", "DesktopAIAssistant", # EXE name
        "--console",                    # Keep console
        "--clean",                      # Clean cache
        "--noconfirm",                  # No confirmation
    ]
    
    # Add all Python files from your project
    python_modules = [
        "ai_pattern_recognition.py",
        "automation_engine.py",
        "data_manager.py",
        "pattern_recognition.py",
        "video_processor.py",
        "workflow_builder.py",
    ]
    
    for module in python_modules:
        if os.path.exists(module):
            cmd.extend(["--add-data", f"{module};."])
            print(f"  📄 Including: {module}")
    
    # Add data folder if exists
    if os.path.exists("data"):
        cmd.extend(["--add-data", "data;data"])
        print(f"  📁 Including: data/")
    
    # Add hidden imports
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Main script
    cmd.append("launcher.py")
    
    print("\n  🚀 Running PyInstaller (this may take a few minutes)...\n")
    
    # Run build
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n  ✅ BUILD SUCCESSFUL!")
        return True
    else:
        print("\n  ❌ BUILD FAILED!")
        return False

def get_folder_size(folder):
    """Calculate folder size in MB"""
    total = 0
    try:
        for root, dirs, files in os.walk(folder):
            for f in files:
                fp = os.path.join(root, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    except:
        pass
    return total / (1024 * 1024)

def create_portable_package():
    """Create a portable package with all files"""
    print_banner("📦 CREATING PORTABLE PACKAGE")
    
    exe_path = Path("dist/DesktopAIAssistant.exe")
    
    if not exe_path.exists():
        print("  ❌ EXE not found in dist/ folder")
        return False
    
    # Create package folder
    package_name = "DesktopAIAssistant_Portable"
    package_path = Path(package_name)
    
    if package_path.exists():
        shutil.rmtree(package_path)
    
    package_path.mkdir()
    print(f"  📁 Created: {package_name}/")
    
    # Copy EXE
    shutil.copy(exe_path, package_path / "DesktopAIAssistant.exe")
    exe_size = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"  ✅ Copied EXE ({exe_size:.2f} MB)")
    
    # Copy data folder if exists
    if os.path.exists("data"):
        shutil.copytree("data", package_path / "data")
        print(f"  ✅ Copied: data/")
    
    # Create README
    readme = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                  DESKTOP AI ASSISTANT - Portable                     ║
╚══════════════════════════════════════════════════════════════════════╝

Version: 1.0
Built: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════════════════

🚀 QUICK START:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Double-click: DesktopAIAssistant.exe
2. Follow the menu options

═══════════════════════════════════════════════════════════════════════

📋 MAIN FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Screen Recording (2 FPS)
✅ Audio Recording with Transcription
✅ Video Processing & Key Frame Extraction
✅ AI Pattern Recognition (Ollama)
✅ Workflow Automation
✅ Smart Data Management

═══════════════════════════════════════════════════════════════════════

⚙️ SYSTEM REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Windows 10/11 (64-bit)
• 4GB RAM minimum (8GB recommended)
• Microphone (for audio recording)
• Internet connection (for AI features)
• Ollama installed (for AI analysis)

═══════════════════════════════════════════════════════════════════════

🤖 AI SETUP (REQUIRED FOR AI FEATURES):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Download Ollama from: https://ollama.ai
2. Install Ollama
3. Open Command Prompt and run:
   
   ollama pull llama3.2:3b

4. Keep Ollama running in the background

═══════════════════════════════════════════════════════════════════════

📁 FOLDER STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DesktopAIAssistant_Portable/
├── DesktopAIAssistant.exe    ← Main application
├── README.txt                 ← This file
├── QUICKSTART.txt             ← Quick guide
└── data/                      ← All your data (auto-created)
    ├── video/                 ← Recorded videos
    ├── audio/                 ← Audio clips
    ├── transcripts/           ← Audio transcripts
    ├── processed/             ← Processed data
    ├── workflows/             ← Saved workflows
    └── patterns/              ← AI insights

═══════════════════════════════════════════════════════════════════════

🎮 HOW TO USE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: START RECORDING
   • Choose option 1 from main menu
   • Press Enter to start
   • Perform your task while speaking
   • Press 'q' to stop recording

STEP 2: PROCESS RECORDING
   • Choose option 3 to process latest recording
   • Wait for video processing to complete

STEP 3: AI ANALYSIS
   • Choose option 5 for AI pattern recognition
   • Get automation suggestions

STEP 4: CREATE AUTOMATION
   • Choose option 7 to create workflows
   • Execute workflows with option 8

═══════════════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Recording fails:
   → Check microphone permissions
   → Run as Administrator

❌ AI analysis fails:
   → Make sure Ollama is running
   → Check: http://localhost:11434

❌ Automation fails:
   → Run as Administrator
   → Disable antivirus temporarily

❌ Out of disk space:
   → Use option 10 (Storage Manager)
   → Delete old recordings

═══════════════════════════════════════════════════════════════════════

⚠️ IMPORTANT NOTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• All data is stored locally in 'data/' folder
• No data is sent to external servers (except Ollama locally)
• First run may take longer to initialize
• Keep all files together in the same folder
• Backup your 'data/' folder regularly

═══════════════════════════════════════════════════════════════════════

📧 SUPPORT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For issues, questions, or feedback:
Contact the developer

═══════════════════════════════════════════════════════════════════════

📄 LICENSE:
Personal use only. Do not redistribute without permission.

═══════════════════════════════════════════════════════════════════════
"""
    
    with open(package_path / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"  ✅ Created README.txt")
    
    # Create Quick Start
    quickstart = """
═══════════════════════════════════════════════════════════════════════
                         QUICK START GUIDE
═══════════════════════════════════════════════════════════════════════

🎯 5-MINUTE SETUP:

1. Install Ollama (AI Engine):
   • Visit: https://ollama.ai
   • Download and install
   • Open CMD and run: ollama pull llama3.2:3b
   • Keep it running

2. Run the App:
   • Double-click: DesktopAIAssistant.exe
   • Wait for menu to appear

3. First Recording:
   • Choose option: 1 (Start recording)
   • Press Enter to start
   • Talk and perform a task (30-60 seconds)
   • Press 'q' to stop

4. Process & Analyze:
   • Choose option: 3 (Process recording)
   • Wait for processing
   • Choose option: 5 (AI Analysis)
   • Get automation insights!

═══════════════════════════════════════════════════════════════════════

📋 MENU OPTIONS EXPLAINED:

1. Start recording          → Begin new screen+audio capture
2. View recordings          → See all your recordings
3. Process latest          → Analyze newest recording
4. Process specific        → Choose which to analyze
5. AI Analysis             → Get AI insights & suggestions
6. View insights           → See past AI analysis
7. Create workflow         → Build automation
8. Execute automation      → Run saved workflows
9. Workflow manager        → Manage all workflows
10. Storage manager        → Clean up old files
11. System status          → Check health
12. Exit                   → Close app

═══════════════════════════════════════════════════════════════════════

💡 TIPS FOR BEST RESULTS:

✅ Recording:
   • Speak clearly and describe what you're doing
   • Record complete tasks (start to finish)
   • 30-60 seconds is ideal
   • Avoid background noise

✅ AI Analysis:
   • Make sure Ollama is running
   • Record repetitive tasks for better insights
   • Review AI suggestions before automating

✅ Automation:
   • Test workflows in safe environment first
   • Use FAILSAFE: Move mouse to corner to stop
   • Start with simple workflows

═══════════════════════════════════════════════════════════════════════

❓ COMMON QUESTIONS:

Q: Where is my data stored?
A: In the 'data/' folder, all stored locally

Q: Does it upload my recordings?
A: No! Everything stays on your computer

Q: Why do I need Ollama?
A: For AI pattern recognition and suggestions

Q: Can I use it without internet?
A: Yes for recording, but AI needs Ollama running

Q: Is it safe to automate?
A: Yes, but always test first and use failsafe

═══════════════════════════════════════════════════════════════════════

Enjoy! 🚀
"""
    
    with open(package_path / "QUICKSTART.txt", "w", encoding="utf-8") as f:
        f.write(quickstart)
    print(f"  ✅ Created QUICKSTART.txt")
    
    # Calculate total size
    total_size = get_folder_size(package_path)
    
    print(f"\n  📦 Package size: {total_size:.2f} MB")
    print(f"  📁 Location: {package_path}/")
    
    return True

def show_final_summary():
    """Show final build summary"""
    print_banner("🎉 BUILD COMPLETE!")
    
    exe_path = Path("dist/DesktopAIAssistant.exe")
    package_path = Path("DesktopAIAssistant_Portable")
    
    if exe_path.exists():
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n  ✅ EXE Created:")
        print(f"     Location: dist/DesktopAIAssistant.exe")
        print(f"     Size: {exe_size:.2f} MB")
    
    if package_path.exists():
        pkg_size = get_folder_size(package_path)
        print(f"\n  ✅ Portable Package Created:")
        print(f"     Location: DesktopAIAssistant_Portable/")
        print(f"     Size: {pkg_size:.2f} MB")
    
    print("\n" + "="*70)
    print("  📤 TO SHARE WITH OTHERS:")
    print("="*70)
    print("\n  Option 1 (Recommended):")
    print("    Zip the 'DesktopAIAssistant_Portable' folder")
    print("    Send the ZIP file")
    print("    Recipients: Extract and run DesktopAIAssistant.exe")
    
    print("\n  Option 2 (Smaller):")
    print("    Send just: dist/DesktopAIAssistant.exe")
    print("    Recipients: Create 'data' folder manually")
    
    print("\n" + "="*70)
    print("  ⚠️  IMPORTANT REMINDER:")
    print("="*70)
    print("\n  Recipients MUST install Ollama for AI features:")
    print("    1. Download from: https://ollama.ai")
    print("    2. Install Ollama")
    print("    3. Run: ollama pull llama3.2:3b")
    
    print("\n" + "="*70)
    print("  ✅ Next Steps:")
    print("="*70)
    print("\n  1. Test the EXE: dist/DesktopAIAssistant.exe")
    print("  2. Create ZIP of portable package")
    print("  3. Share with others!")
    print("\n")

def main():
    """Main build process"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║         DESKTOP AI ASSISTANT - EXE BUILDER                           ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    # Step 1: Verify files
    if not verify_project_files():
        print("\n  ❌ Some required files are missing!")
        input("\n  Press Enter to exit...")
        return
    
    # Step 2: Install PyInstaller
    if not install_pyinstaller():
        input("\n  Press Enter to exit...")
        return
    
    # Step 3: Clean old builds
    clean_build()
    
    # Step 4: Confirm build
    print_banner("🚀 READY TO BUILD")
    print("\n  This will create:")
    print("    • Single EXE file (dist/DesktopAIAssistant.exe)")
    print("    • Portable package (DesktopAIAssistant_Portable/)")
    print("\n  Build time: 2-5 minutes")
    
    confirm = input("\n  Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n  👋 Build cancelled")
        return
    
    # Step 5: Build EXE
    if not build_exe():
        print("\n  ❌ Build failed!")
        input("\n  Press Enter to exit...")
        return
    
    # Step 6: Create portable package
    print("\n")
    create_pkg = input("  📦 Create portable package? (y/n): ").strip().lower()
    if create_pkg == 'y':
        create_portable_package()
    
    # Step 7: Show summary
    show_final_summary()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()