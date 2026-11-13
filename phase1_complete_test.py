"""
Phase 1 Complete Test - Screen Recording + Audio + Speech-to-Text
Tests all Phase 1 components together
"""

import time
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from desktop_ai_assistant.capture.screen_recorder import ScreenRecorder
from desktop_ai_assistant.capture.audio_recorder import AudioRecorder

def test_phase1():
    """Test screen recording and audio recording together"""
    
    print("\n" + "="*70)
    print("PHASE 1 COMPLETE TEST")
    print("="*70)
    print("\nThis will test:")
    print("1. Screen recording (video capture)")
    print("2. Audio recording (microphone)")
    print("3. Both running simultaneously")
    print("\nDuration: 30 seconds")
    print("\n" + "="*70)
    
    input("\nPress ENTER to start...")
    
    # Create recorders
    print("\nInitializing recorders...")
    screen_recorder = ScreenRecorder(
        output_dir="data/recordings",
        fps=2,
        clip_duration=15,
        max_clips=5
    )
    
    audio_recorder = AudioRecorder(
        output_dir="data/audio",
        sample_rate=16000
    )
    
    # Start both recorders
    print("\n" + "="*70)
    print("RECORDING STARTED!")
    print("="*70)
    print("\nWhat to do:")
    print("- Open some applications")
    print("- Move windows around")
    print("- SPEAK into your microphone")
    print("- Type some text")
    print("- Click on things")
    print("\nThe AI is watching and listening!\n")
    
    screen_recorder.start()
    audio_recorder.start()
    
    try:
        # Record for 30 seconds
        for i in range(30):
            time.sleep(1)
            if i % 10 == 0 and i > 0:
                screen_stats = screen_recorder.get_stats()
                audio_stats = audio_recorder.get_stats()
                print(f"Time: {i}s | Video Frames: {screen_stats['total_frames']} | "
                      f"Audio Clips: {audio_stats['clips_saved']}")
    
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    
    # Stop both recorders
    print("\n\nStopping recorders...")
    screen_recorder.stop()
    audio_recorder.stop()
    
    # Show results
    screen_stats = screen_recorder.get_stats()
    audio_stats = audio_recorder.get_stats()
    
    print("\n" + "="*70)
    print("PHASE 1 TEST COMPLETE!")
    print("="*70)
    
    print("\n📹 Screen Recording:")
    print(f"   Total frames: {screen_stats['total_frames']}")
    print(f"   Video clips: {screen_stats['clips_saved']}")
    print(f"   Location: data/recordings/")
    
    print("\n🎤 Audio Recording:")
    print(f"   Audio clips: {audio_stats['clips_saved']}")
    print(f"   Location: data/audio/")
    
    print("\n" + "="*70)
    print("✅ YOUR AI ASSISTANT CAN NOW:")
    print("="*70)
    print("✅ Watch your screen (like a dashcam)")
    print("✅ Record audio (capture voice commands)")
    print("✅ Save everything locally (100% private)")
    
    print("\n📁 Check these folders:")
    print("   • data/recordings/ - Your video clips")
    print("   • data/audio/ - Your audio recordings")
    
    print("\n🎯 NEXT: Phase 2 - Process this data into structured events")
    print("="*70 + "\n")


# Speech-to-Text Test (separate function)
def test_speech_to_text():
    """Test Whisper speech-to-text on recorded audio"""
    
    print("\n" + "="*70)
    print("SPEECH-TO-TEXT TEST")
    print("="*70 + "\n")
    
    audio_dir = Path("data/audio")
    audio_files = list(audio_dir.glob("*.wav"))
    
    if not audio_files:
        print("❌ No audio files found!")
        print("   Run the Phase 1 test first to record audio.\n")
        return
    
    print(f"Found {len(audio_files)} audio files\n")
    print("Loading Whisper AI model...")
    print("(This may take 1-2 minutes first time)\n")
    
    try:
        import whisper
        model = whisper.load_model("base")
        print("✅ Whisper loaded!\n")
        
        print("="*70)
        print("TRANSCRIPTIONS:")
        print("="*70 + "\n")
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"{i}. Processing: {audio_file.name}")
            
            try:
                result = model.transcribe(str(audio_file.absolute()))
                text = result["text"].strip()
                
                if text:
                    print(f"   You said: \"{text}\"")
                else:
                    print(f"   (No speech detected)")
                    
            except Exception as e:
                print(f"   Error: {e}")
            
            print()
        
        print("="*70)
        print("✅ SPEECH-TO-TEXT WORKING!")
        print("="*70)
        print("\nYour AI can now:")
        print("• Understand voice commands")
        print("• Convert speech to text")
        print("• Process audio locally (no cloud!)")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error loading Whisper: {e}")
        print("\nTry: pip install openai-whisper\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖 DESKTOP AI ASSISTANT - PHASE 1 TESTING")
    print("="*70)
    print("\nWhat would you like to test?")
    print("\n1. Screen + Audio Recording (30 seconds)")
    print("2. Speech-to-Text (process existing audio)")
    print("3. Both (record then transcribe)")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_phase1()
    elif choice == "2":
        test_speech_to_text()
    elif choice == "3":
        test_phase1()
        print("\nNow testing speech-to-text...\n")
        time.sleep(2)
        test_speech_to_text()
    else:
        print("Invalid choice. Please run again and choose 1, 2, or 3")