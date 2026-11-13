import whisper
import soundfile as sf
import numpy as np
from pathlib import Path

def test_whisper_with_soundfile():
    """Test Whisper with soundfile library (no FFmpeg needed)"""
    
    print("Loading Whisper...")
    model = whisper.load_model("base")
    print("Model loaded!")
    
    # Find the audio file
    audio_file = Path("data/audio/audio_20251026_104438.wav")
    print(f"\nProcessing: {audio_file}")
    print(f"File exists: {audio_file.exists()}")
    
    if not audio_file.exists():
        print("❌ Audio file not found!")
        return
    
    # Load audio with soundfile instead of FFmpeg
    print("\nLoading audio with soundfile...")
    audio_data, sample_rate = sf.read(str(audio_file))
    
    # Convert to mono if stereo
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)
    
    # Resample to 16kHz if needed (Whisper expects 16kHz)
    if sample_rate != 16000:
        print(f"Resampling from {sample_rate}Hz to 16000Hz...")
        import librosa
        audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
    
    # Convert to float32
    audio_data = audio_data.astype(np.float32)
    
    print("Transcribing...")
    result = model.transcribe(audio_data, fp16=False)
    
    print("\n" + "="*50)
    print("📝 TRANSCRIPTION:")
    print("="*50)
    print(result["text"])
    print("="*50)
    
    # Save to file
    output_file = Path("data/transcripts") / f"{audio_file.stem}_transcript.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        f.write(result["text"])
    
    print(f"\n✅ Saved to: {output_file}")

if __name__ == "__main__":
    test_whisper_with_soundfile()