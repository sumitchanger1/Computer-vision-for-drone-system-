"""Screen Recorder Module"""

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
