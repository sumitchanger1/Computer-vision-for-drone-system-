"""
Audio Processor - Converts speech to text using Whisper
"""

import whisper
import numpy as np
from pathlib import Path
import wave


class AudioProcessor:
    """Processes audio files and converts speech to text"""
    
    def __init__(self, model_name="base"):
        """
        Initialize Whisper model
        model_name: 'tiny', 'base', 'small', 'medium', 'large'
        'base' is good balance of speed and accuracy
        """
        print(f"Loading Whisper model '{model_name}'...")
        print("(First time will download ~140MB model)")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded!")
        
    def transcribe_file(self, audio_path):
        """
        Convert audio file to text
        
        Args:
            audio_path: Path to WAV audio file
            
        Returns:
            dict with 'text' and 'language'
        """
        print(f"Transcribing: {Path(audio_path).name}...")
        
        # Transcribe using Whisper
        result = self.model.transcribe(str(audio_path), language="en")
        
        transcription = {
            'text': result['text'].strip(),
            'language': result['language'],
            'file': str(audio_path)
        }
        
        return transcription
    
    def transcribe_folder(self, folder_path):
        """
        Transcribe all WAV files in a folder
        
        Args:
            folder_path: Path to folder containing audio files
            
        Returns:
            List of transcriptions
        """
        folder = Path(folder_path)
        audio_files = list(folder.glob("*.wav"))
        
        if not audio_files:
            print(f"No audio files found in {folder}")
            return []
        
        print(f"\nFound {len(audio_files)} audio files")
        print("=" * 60)
        
        transcriptions = []
        
        for audio_file in audio_files:
            try:
                result = self.transcribe_file(audio_file)
                transcriptions.append(result)
                
                print(f"\nFile: {audio_file.name}")
                print(f"Text: {result['text']}")
                print("-" * 60)
                
            except Exception as e:
                print(f"Error processing {audio_file.name}: {e}")
        
        return transcriptions


# Test the audio processor
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AUDIO PROCESSOR TEST - Speech to Text")
    print("=" * 60 + "\n")
    
    # Check if audio files exist
    audio_dir = Path("data/audio")
    audio_files = list(audio_dir.glob("*.wav"))
    
    if not audio_files:
        print("No audio files found!")
        print("Please run audio_recorder.py first to record some audio.\n")
    else:
        print(f"Found {len(audio_files)} audio files to process\n")
        
        # Create processor
        processor = AudioProcessor(model_name="base")
        
        # Transcribe all audio files
        results = processor.transcribe_folder("data/audio")
        
        # Summary
        print("\n" + "=" * 60)
        print("TRANSCRIPTION COMPLETE!")
        print("=" * 60)
        print(f"\nProcessed {len(results)} files")
        
        if results:
            print("\nAll transcriptions:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['text']}")
        
        print("\n" + "=" * 60)