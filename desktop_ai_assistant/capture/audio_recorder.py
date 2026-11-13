"""
Audio Recorder Module - Records microphone and converts speech to text
"""

import time
import wave
import numpy as np
from datetime import datetime
from pathlib import Path
from threading import Thread, Event
import sounddevice as sd

class AudioRecorder:
    """Records audio from microphone"""
    
    def __init__(self, output_dir="data/audio", sample_rate=16000, channels=1):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = Event()
        self.recording_thread = None
        self.audio_buffer = []
        self.clips_saved = []
        
    def start(self):
        """Start recording audio"""
        if self.is_recording.is_set():
            print("Audio recording already in progress!")
            return
        
        print("Starting audio recording...")
        self.is_recording.set()
        self.recording_thread = Thread(target=self._record_loop, daemon=True)
        self.recording_thread.start()
        print("Audio recording started!")
        
    def stop(self):
        """Stop recording audio"""
        if not self.is_recording.is_set():
            return
        
        print("Stopping audio recording...")
        self.is_recording.clear()
        if self.recording_thread:
            self.recording_thread.join(timeout=5)
        
        # Save any remaining audio
        if len(self.audio_buffer) > 0:
            self._save_audio_clip()
        
        print("Audio recording stopped!")
        
    def _record_loop(self):
        """Main recording loop"""
        chunk_duration = 10  # Save audio every 10 seconds
        
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'
        ) as stream:
            
            chunk_start = time.time()
            
            while self.is_recording.is_set():
                # Read audio chunk (0.5 second chunks)
                audio_chunk = stream.read(int(self.sample_rate * 0.5))[0]
                self.audio_buffer.extend(audio_chunk)
                
                # Save clip every 10 seconds
                if time.time() - chunk_start >= chunk_duration:
                    self._save_audio_clip()
                    self.audio_buffer = []
                    chunk_start = time.time()
    
    def _save_audio_clip(self):
        """Save audio buffer to WAV file"""
        if len(self.audio_buffer) == 0:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = self.output_dir / f"audio_{timestamp}.wav"
        
        # Convert to numpy array
        audio_data = np.array(self.audio_buffer, dtype=np.int16)
        
        # Save as WAV file
        with wave.open(str(audio_path), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        
        self.clips_saved.append(audio_path)
        print(f"Audio clip saved: {audio_path.name}")
        
        # Cleanup old clips (keep last 10)
        if len(self.clips_saved) > 10:
            old_clip = self.clips_saved.pop(0)
            try:
                old_clip.unlink()
                print(f"Removed old audio clip: {old_clip.name}")
            except:
                pass
    
    def get_stats(self):
        """Get recording statistics"""
        return {
            'is_recording': self.is_recording.is_set(),
            'clips_saved': len(self.clips_saved),
            'buffer_size': len(self.audio_buffer)
        }


# Test the audio recorder
if __name__ == "__main__":
    print("\nAudio Recorder Test")
    print("=" * 60)
    print("Testing microphone recording...")
    print("Speak into your microphone!\n")
    
    recorder = AudioRecorder()
    recorder.start()
    
    try:
        # Record for 20 seconds
        for i in range(20):
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                stats = recorder.get_stats()
                print(f"Time: {i}s | Clips saved: {stats['clips_saved']}")
    
    except KeyboardInterrupt:
        print("\nStopped by user")
    
    recorder.stop()
    
    stats = recorder.get_stats()
    print("\n" + "=" * 60)
    print("Test Complete!")
    print(f"Audio clips saved: {stats['clips_saved']}")
    print("\nCheck folder: data/audio/")
    print("=" * 60)