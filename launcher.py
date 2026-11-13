"""
Desktop AI Assistant - Main Launcher
All-in-one interface for the complete system
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Display application banner"""
    print("\n" + "="*70)
    print("🤖 DESKTOP AI ASSISTANT - MVP")
    print("="*70)
    print("   AI-Powered Desktop Automation System")
    print("   Records → Processes → Learns → Automates")
    print("="*70)

def check_dependencies():
    """Check if all required modules are available"""
    required = {
        'whisper': 'openai-whisper',
        'cv2': 'opencv-python',
        'pyautogui': 'pyautogui',
        'sounddevice': 'sounddevice',
        'soundfile': 'soundfile'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    return True

def main_menu():
    """Main application menu"""
    
    print_banner()
    
    # Skip dependency check when running as EXE
    if not getattr(sys, 'frozen', False):
        # Running as script
        if not check_dependencies():
            print("\n❌ Please install missing dependencies first!")
            input("\nPress Enter to exit...")
            return
    else:
        # Running as EXE - assume dependencies are available
        print("✅ Running as executable\n")
    
    while True:
        print("\n" + "="*70)
        print("📋 MAIN MENU")
        print("="*70)
        print("\n🎬 RECORDING:")
        print("   1. Start new recording session")
        print("   2. View recordings")
        
        print("\n⚙️  PROCESSING:")
        print("   3. Process latest recording")
        print("   4. Process specific recording")
        
        print("\n🧠 AI ANALYSIS:")
        print("   5. Analyze with AI (Phase 3)")
        print("   6. View AI insights")
        
        print("\n🤖 AUTOMATION:")
        print("   7. Create workflow")
        print("   8. Execute automation")
        print("   9. Workflow manager")
        
        print("\n💾 MANAGEMENT:")
        print("   10. Storage manager")
        print("   11. System status")
        
        print("\n❌ EXIT:")
        print("   12. Exit application")
        
        print("="*70)
        
        choice = input("\n👉 Select option (1-12): ").strip()
        
        try:
            if choice == '1':
                start_recording()
            elif choice == '2':
                view_recordings()
            elif choice == '3':
                process_latest_recording()
            elif choice == '4':
                process_specific_recording()
            elif choice == '5':
                analyze_with_ai()
            elif choice == '6':
                view_ai_insights()
            elif choice == '7':
                create_workflow()
            elif choice == '8':
                execute_automation()
            elif choice == '9':
                workflow_manager()
            elif choice == '10':
                storage_manager()
            elif choice == '11':
                show_system_status()
            elif choice == '12':
                print("\n👋 Thank you for using Desktop AI Assistant!")
                print("   Exiting...\n")
                break
            else:
                print("\n❌ Invalid option! Please choose 1-12")
                input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

def start_recording():
    """Start recording session"""
    print("\n" + "="*70)
    print("🎬 STARTING RECORDING SESSION")
    print("="*70)
    
    try:
        # Import here to avoid loading if not needed
        import subprocess
        
        print("\n📹 Recording will start in 3 seconds...")
        print("   Press 'q' to stop recording")
        
        input("\nPress Enter to start...")
        
        # Run main.py
        subprocess.run([sys.executable, "main.py"])
        
    except Exception as e:
        print(f"\n❌ Recording failed: {e}")
    
    input("\nPress Enter to return to menu...")

def view_recordings():
    """View all recordings"""
    print("\n" + "="*70)
    print("📂 YOUR RECORDINGS")
    print("="*70)
    
    video_dir = Path("data/video")
    
    if not video_dir.exists():
        print("\n⚠️  No recordings found yet!")
        input("\nPress Enter to return...")
        return
    
    videos = sorted(video_dir.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not videos:
        print("\n⚠️  No video files found!")
    else:
        print(f"\n📊 Total recordings: {len(videos)}\n")
        for i, video in enumerate(videos, 1):
            size_mb = video.stat().st_size / (1024 * 1024)
            print(f"   {i}. {video.name} ({size_mb:.2f} MB)")
    
    input("\nPress Enter to return...")

def process_latest_recording():
    """Process the latest recording"""
    print("\n" + "="*70)
    print("⚙️  PROCESSING LATEST RECORDING")
    print("="*70)
    
    try:
        import subprocess
        
        print("\n🔄 Running video processor...")
        subprocess.run([sys.executable, "video_processor.py"])
        
    except Exception as e:
        print(f"\n❌ Processing failed: {e}")
    
    input("\nPress Enter to return...")

def process_specific_recording():
    """Process a specific recording"""
    print("\n⚠️  Feature: Process specific recording")
    print("   Use option 3 to process latest, or run video_processor.py directly")
    input("\nPress Enter to return...")

def analyze_with_ai():
    """Analyze with AI"""
    print("\n" + "="*70)
    print("🧠 AI PATTERN ANALYSIS")
    print("="*70)
    
    # Check if AI version exists
    if Path("ai_pattern_recognition.py").exists():
        try:
            import subprocess
            subprocess.run([sys.executable, "ai_pattern_recognition.py"])
        except Exception as e:
            print(f"\n❌ AI analysis failed: {e}")
    else:
        try:
            import subprocess
            subprocess.run([sys.executable, "pattern_recognition.py"])
        except Exception as e:
            print(f"\n❌ Analysis failed: {e}")
    
    input("\nPress Enter to return...")

def view_ai_insights():
    """View AI insights"""
    print("\n" + "="*70)
    print("📊 AI INSIGHTS")
    print("="*70)
    
    patterns_dir = Path("data/patterns")
    
    if not patterns_dir.exists():
        print("\n⚠️  No AI insights yet! Analyze a recording first.")
        input("\nPress Enter to return...")
        return
    
    insights = list(patterns_dir.glob("*_insights.json"))
    
    if not insights:
        print("\n⚠️  No insights found!")
    else:
        print(f"\n📈 Found {len(insights)} analysis results:\n")
        for insight in insights:
            print(f"   • {insight.name}")
    
    input("\nPress Enter to return...")

def create_workflow():
    """Create automation workflow"""
    print("\n" + "="*70)
    print("🎨 WORKFLOW CREATOR")
    print("="*70)
    
    try:
        import subprocess
        subprocess.run([sys.executable, "workflow_builder.py"])
    except Exception as e:
        print(f"\n❌ Failed: {e}")
    
    input("\nPress Enter to return...")

def execute_automation():
    """Execute automation"""
    print("\n" + "="*70)
    print("🤖 EXECUTE AUTOMATION")
    print("="*70)
    
    print("\nChoose automation system:")
    print("1. Workflow-based automation (integrated)")
    print("2. Computer Use Platform (demo capabilities)")
    
    choice = input("\nChoice (1-2): ").strip()
    
    try:
        import subprocess
        if choice == '2':
            subprocess.run([sys.executable, "phase4_computer_use_platform.py"])
        else:
            subprocess.run([sys.executable, "workflow_builder.py"])
    except Exception as e:
        print(f"\n❌ Failed: {e}")
    
    input("\nPress Enter to return...")

def workflow_manager():
    """Workflow manager"""
    print("\n" + "="*70)
    print("📋 WORKFLOW MANAGER")
    print("="*70)
    
    try:
        import subprocess
        subprocess.run([sys.executable, "workflow_builder.py"])
    except Exception as e:
        print(f"\n❌ Failed: {e}")
    
    input("\nPress Enter to return...")

def storage_manager():
    """Storage management"""
    print("\n" + "="*70)
    print("💾 STORAGE MANAGER")
    print("="*70)
    
    try:
        import subprocess
        subprocess.run([sys.executable, "data_manager.py"])
    except Exception as e:
        print(f"\n❌ Failed: {e}")
    
    input("\nPress Enter to return...")

def show_system_status():
    """Show system status"""
    print("\n" + "="*70)
    print("📊 SYSTEM STATUS")
    print("="*70)
    
    # Check all components
    components = {
        "Recording System": Path("main.py").exists(),
        "Video Processor": Path("video_processor.py").exists(),
        "Pattern Recognition": Path("pattern_recognition.py").exists(),
        "Automation Engine": Path("automation_engine.py").exists(),
        "Workflow Builder": Path("workflow_builder.py").exists(),
        "Data Manager": Path("data_manager.py").exists()
    }
    
    print("\n✅ Component Status:\n")
    for component, status in components.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}")
    
    # Check data folders
    print("\n📁 Data Folders:\n")
    folders = ["audio", "video", "transcripts", "processed", "workflows", "patterns"]
    for folder in folders:
        folder_path = Path("data") / folder
        exists = folder_path.exists()
        status_icon = "✅" if exists else "❌"
        
        if exists:
            file_count = len(list(folder_path.rglob("*")))
            print(f"   {status_icon} {folder} ({file_count} files)")
        else:
            print(f"   {status_icon} {folder}")
    
    input("\nPress Enter to return...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        input("\nPress Enter to exit...")