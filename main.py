"""
Desktop AI Assistant - Phase 1: Recording System
Integrated with launcher.py
"""

import sys
import time
import os
from pathlib import Path
from datetime import datetime
import keyboard

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import our working modules
from desktop_ai_assistant.capture.screen_recorder import ScreenRecorder
from desktop_ai_assistant.capture.audio_recorder import AudioRecorder

def main():
    """Main recording function"""
    
    print("\n" + "="*70)
    print("🎬 PHASE 1: RECORDING SESSION")
    print("="*70)
    print("\n📋 What will be recorded:")
    print("   • Your screen (2 FPS - efficient)")
    print("   • Your microphone audio")
    print("   • Everything saved locally")
    
    print("\n⚙️  Settings:")
    print("   • Video: 2 FPS, 30-second clips")
    print("   • Audio: 16kHz, 10-second clips")
    print("   • Location: data/video/ and data/audio/")
    
    print("\n🔴 Recording Controls:")
    print("   • Press 'q' to stop recording")
    print("   • Or it will auto-stop after 2 minutes")
    
    print("\n" + "="*70)
    
    duration = input("\nRecording duration in seconds (default 60): ").strip()
    if not duration or not duration.isdigit():
        duration = 60
    else:
        duration = int(duration)
    
    print(f"\n✅ Will record for {duration} seconds")
    input("\nPress ENTER to start recording...")
    
    # Create recorders with correct paths for launcher
    screen_recorder = ScreenRecorder(
        output_dir="data/video",
        fps=2,
        clip_duration=30,
        max_clips=10
    )
    
    audio_recorder = AudioRecorder(
        output_dir="data/audio",
        sample_rate=16000
    )
    
    # Start recording
    print("\n" + "="*70)
    print("🔴 RECORDING STARTED!")
    print("="*70)
    print("\n💡 Tips:")
    print("   • Speak clearly into your microphone")
    print("   • Describe what you're doing")
    print("   • Perform your task normally")
    print(f"\n⏱️  Recording for {duration} seconds...")
    print("   Press 'q' to stop early\n")
    
    screen_recorder.start()
    audio_recorder.start()
    
    start_time = time.time()
    
    try:
        # Record for specified duration
        while time.time() - start_time < duration:
            # Check if 'q' was pressed
            if keyboard.is_pressed('q'):
                print("\n\n⚠️  Stopping early (q pressed)...")
                break
            
            elapsed = int(time.time() - start_time)
            
            # Show progress every 10 seconds
            if elapsed % 10 == 0 and elapsed > 0:
                screen_stats = screen_recorder.get_stats()
                audio_stats = audio_recorder.get_stats()
                remaining = duration - elapsed
                print(f"⏱️  {elapsed}s / {duration}s | "
                      f"Video: {screen_stats['total_frames']} frames | "
                      f"Audio: {audio_stats['clips_saved']} clips | "
                      f"Remaining: {remaining}s")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    
    # Stop recorders
    print("\n\n🛑 Stopping recorders...")
    screen_recorder.stop()
    audio_recorder.stop()
    
    # Show final stats
    screen_stats = screen_recorder.get_stats()
    audio_stats = audio_recorder.get_stats()
    
    print("\n" + "="*70)
    print("✅ RECORDING COMPLETE!")
    print("="*70)
    
    print("\n📊 Recording Statistics:")
    print(f"   • Video frames: {screen_stats['total_frames']}")
    print(f"   • Video clips: {screen_stats['clips_saved']}")
    print(f"   • Audio clips: {audio_stats['clips_saved']}")
    print(f"   • Duration: {int(time.time() - start_time)} seconds")
    
    print("\n💾 Files saved to:")
    print("   • Videos: data/video/")
    print("   • Audio: data/audio/")
    
    print("\n🎯 Next Steps:")
    print("   1. Return to launcher")
    print("   2. Choose option 3: Process recording")
    print("   3. Choose option 5: AI Analysis")
    
    print("\n" + "="*70)
    
    # Transcribe audio files
    print("\n🎤 Would you like to transcribe audio now? (y/n): ", end='')
    transcribe = input().strip().lower()
    
    if transcribe == 'y':
        transcribe_audio()
    
    print("\n✅ Done! Returning to launcher...\n")

def transcribe_audio():
    """Transcribe recorded audio using Whisper"""
    
    print("\n" + "="*70)
    print("🎤 TRANSCRIBING AUDIO")
    print("="*70 + "\n")
    
    try:
        # Configure ffmpeg
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        os.environ["PATH"] = str(Path(ffmpeg_exe).parent) + os.pathsep + os.environ.get("PATH", "")
        
        print("Loading Whisper AI model...")
        import whisper
        model = whisper.load_model("base")
        print("✅ Whisper loaded!\n")
        
        # Get audio files
        audio_dir = Path("data/audio")
        audio_files = sorted(audio_dir.glob("*.wav"))
        
        if not audio_files:
            print("⚠️  No audio files found!")
            return
        
        print(f"Found {len(audio_files)} audio files\n")
        
        # Create transcripts directory
        transcripts_dir = Path("data/transcripts")
        transcripts_dir.mkdir(exist_ok=True)
        
        all_transcripts = []
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"{i}/{len(audio_files)} Processing: {audio_file.name}")
            
            try:
                result = model.transcribe(
                    str(audio_file.absolute()),
                    language="en",
                    fp16=False
                )
                text = result["text"].strip()
                
                if text:
                    print(f"   ✅ \"{text[:60]}...\"\n")
                    all_transcripts.append({
                        "file": audio_file.name,
                        "text": text,
                        "timestamp": audio_file.stem.replace("audio_", "")
                    })
                else:
                    print(f"   (Silent)\n")
            
            except Exception as e:
                print(f"   ❌ Error: {e}\n")
        
        # Save transcripts
        if all_transcripts:
            import json
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            transcript_file = transcripts_dir / f"transcript_{timestamp}.json"
            
            with open(transcript_file, 'w') as f:
                json.dump(all_transcripts, f, indent=2)
            
            print(f"✅ Transcripts saved to: {transcript_file}")
            print(f"   Total transcriptions: {len(all_transcripts)}")
        
    except Exception as e:
        print(f"❌ Transcription failed: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")