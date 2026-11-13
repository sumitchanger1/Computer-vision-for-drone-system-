"""Whisper Test with Proper ffmpeg Path"""
import os
from pathlib import Path
import imageio_ffmpeg

# Set ffmpeg path for Whisper
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = str(Path(ffmpeg_exe).parent) + os.pathsep + os.environ.get("PATH", "")
print(f"✅ ffmpeg configured: {ffmpeg_exe}\n")

import whisper

print("Loading Whisper...")
model = whisper.load_model("base")
print("✅ Whisper loaded!\n")

audio_dir = Path("data/audio")
audio_files = sorted(audio_dir.glob("*.wav"))

print(f"Found {len(audio_files)} files\n")
print("="*70)

for i, audio_file in enumerate(audio_files, 1):
    print(f"\n{i}. {audio_file.name}")
    
    try:
        result = model.transcribe(
            str(audio_file.absolute()),
            language="en",
            fp16=False
        )
        
        text = result["text"].strip()
        
        if text:
            print(f"   ✅ \"{text}\"")
        else:
            print(f"   (Silent)")
    
    except Exception as e:
        print(f"   ❌ {e}")

print("\n" + "="*70)
print("Done!")