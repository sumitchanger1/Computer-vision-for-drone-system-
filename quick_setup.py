"""
COMPLETE SETUP SCRIPT - ALL IN ONE!
Just run: python quick_setup.py
"""

import subprocess
import sys
from pathlib import Path
import time

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    dependencies = [
        "mss==9.0.1",
        "opencv-python==4.8.1.78", 
        "Pillow==10.1.0",
        "numpy==1.24.3"
    ]
    
    for dep in dependencies:
        print(f"   Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "-q"])
    
    print("All dependencies installed!\n")

def create_folders():
    """Create project structure"""
    print("Creating folders...")
    folders = [
        "desktop_ai_assistant/core",
        "desktop_ai_assistant/capture",
        "data/recordings",
        "data/screenshots"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {folder}")
    
    init_files = [
        "desktop_ai_assistant/__init__.py",
        "desktop_ai_assistant/core/__init__.py",
        "desktop_ai_assistant/capture/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
    
    print("Folders created!\n")

def create_config_file():
    """Create configuration file"""
    print("Creating config file...")
    
    config_code = '''"""Configuration for AI Assistant"""

class Config:
    # Screen Recording
    SCREEN_FPS = 2
    CLIP_DURATION = 30
    MAX_CLIPS = 10
    
    # Folders
    RECORDINGS_DIR = "data/recordings"
    SCREENSHOTS_DIR = "data/screenshots"

config = Config()
'''
    
    config_path = Path("desktop_ai_assistant/core/config.py")
    config_path.write_text(config_code)
    print("Config created!\n")

def create_recorder_file():
    """Create screen recorder"""
    print("Creating screen recorder...")
    
    recorder_code = '''"""Screen Recorder Module"""

import time
import mss
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
from threading import Thread, Event

class ScreenRecorder:
    def __init__(self, output_dir="data/recordings", fps=2, clip_duration=30, max_clips=10):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fps = fps
        self.clip_duration = clip_duration
        self.max_clips = max_clips
        self.is_recording = Event()
        self.recording_thread = None
        self.total_frames = 0
        self.clips_saved = []
        
    def start(self):
        if self.is_recording.is_set():
            return
        print("Recording started!")
        self.is_recording.set()
        self.recording_thread = Thread(target=self._record_loop, daemon=True)
        self.recording_thread.start()
        
    def stop(self):
        if not self.is_recording.is_set():
            return
        print("Stopping...")
        self.is_recording.clear()
        if self.recording_thread:
            self.recording_thread.join(timeout=5)
        print("Stopped!")
        
    def _record_loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width = int(monitor["width"] * 0.75)
            height = int(monitor["height"] * 0.75)
            frame_delay = 1.0 / self.fps
            clip_start = time.time()
            frame_count = 0
            clip_path, video_writer = self._start_new_clip(width, height)
            
            while self.is_recording.is_set():
                loop_start = time.time()
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                frame = cv2.resize(frame, (width, height))
                video_writer.write(frame)
                frame_count += 1
                self.total_frames += 1
                
                if time.time() - clip_start >= self.clip_duration:
                    video_writer.release()
                    print(f"Saved clip: {frame_count} frames")
                    clip_path, video_writer = self._start_new_clip(width, height)
                    clip_start = time.time()
                    frame_count = 0
                    self._cleanup_old_clips()
                
                elapsed = time.time() - loop_start
                time.sleep(max(0, frame_delay - elapsed))
            
            if video_writer:
                video_writer.release()
    
    def _start_new_clip(self, width, height):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clip_path = self.output_dir / f"clip_{timestamp}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(clip_path), fourcc, self.fps, (width, height))
        self.clips_saved.append(clip_path)
        return clip_path, video_writer
    
    def _cleanup_old_clips(self):
        if len(self.clips_saved) > self.max_clips:
            old_clips = self.clips_saved[:-self.max_clips]
            for clip_path in old_clips:
                try:
                    clip_path.unlink()
                except:
                    pass
            self.clips_saved = self.clips_saved[-self.max_clips:]
    
    def get_stats(self):
        return {
            'is_recording': self.is_recording.is_set(),
            'total_frames': self.total_frames,
            'clips_saved': len(self.clips_saved)
        }
'''
    
    recorder_path = Path("desktop_ai_assistant/capture/screen_recorder.py")
    recorder_path.write_text(recorder_code, encoding='utf-8')
    print("Screen recorder created!\n")

def run_test():
    """Run a test recording"""
    print("\n" + "="*60)
    print("RUNNING TEST RECORDING (30 seconds)")
    print("="*60 + "\n")
    print("Open apps, move windows, do stuff on your computer!")
    print("The AI is learning...\n")
    
    input("Press ENTER to start recording...")
    
    sys.path.insert(0, str(Path.cwd()))
    from desktop_ai_assistant.capture.screen_recorder import ScreenRecorder
    
    recorder = ScreenRecorder(fps=2, clip_duration=10, max_clips=5)
    recorder.start()
    
    print("\nRECORDING NOW!\n")
    
    try:
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                stats = recorder.get_stats()
                print(f"Time: {i}s | Frames: {stats['total_frames']} | Clips: {stats['clips_saved']}")
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    
    recorder.stop()
    
    stats = recorder.get_stats()
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)
    print(f"\nResults:")
    print(f"   Frames captured: {stats['total_frames']}")
    print(f"   Clips saved: {stats['clips_saved']}")
    print(f"\nCheck folder: data/recordings/")
    
    recordings_dir = Path("data/recordings")
    videos = list(recordings_dir.glob("*.mp4"))
    if videos:
        print("\nYour recordings:")
        for video in videos:
            size_mb = video.stat().st_size / (1024 * 1024)
            print(f"   {video.name} ({size_mb:.2f} MB)")
    
    print("\nSUCCESS! Your Desktop AI Assistant is working!\n")

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("DESKTOP AI ASSISTANT - AUTOMATIC SETUP")
    print("="*70 + "\n")
    
    try:
        install_dependencies()
        create_folders()
        create_config_file()
        create_recorder_file()
        
        print("="*70)
        print("SETUP COMPLETE!")
        print("="*70 + "\n")
        
        run_test()
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()