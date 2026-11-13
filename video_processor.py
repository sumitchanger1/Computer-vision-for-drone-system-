import cv2
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from PIL import Image
import hashlib

class VideoProcessor:
    def __init__(self, video_path, output_dir="data/processed"):
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.frames_dir = self.output_dir / "frames"
        self.frames_dir.mkdir(exist_ok=True)
        
        self.json_dir = self.output_dir / "json"
        self.json_dir.mkdir(exist_ok=True)
        
    def extract_key_frames(self, threshold=30, max_frames=100):
        """Extract frames when significant changes occur"""
        
        print(f"🎬 Processing video: {self.video_path.name}")
        
        cap = cv2.VideoCapture(str(self.video_path))
        
        if not cap.isOpened():
            print("❌ Could not open video file")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"📊 Video info:")
        print(f"   FPS: {fps:.2f}")
        print(f"   Total frames: {total_frames}")
        print(f"   Duration: {duration:.2f} seconds")
        
        frames_data = []
        prev_frame = None
        frame_count = 0
        saved_count = 0
        
        print(f"\n🔍 Extracting key frames (threshold={threshold})...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            timestamp = frame_count / fps
            
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                diff_score = np.mean(diff)
                
                if diff_score > threshold or saved_count == 0:
                    frame_info = self._save_frame(frame, timestamp, frame_count, diff_score)
                    frames_data.append(frame_info)
                    saved_count += 1
                    
                    if saved_count % 10 == 0:
                        print(f"   Saved {saved_count} frames...")
                    
                    if saved_count >= max_frames:
                        print(f"   Reached max frames limit ({max_frames})")
                        break
            else:
                frame_info = self._save_frame(frame, timestamp, frame_count, 0)
                frames_data.append(frame_info)
                saved_count += 1
            
            prev_frame = frame.copy()
        
        cap.release()
        
        print(f"\n✅ Extracted {saved_count} key frames from {frame_count} total frames")
        
        return frames_data
    
    def _save_frame(self, frame, timestamp, frame_number, diff_score):
        """Save frame and return metadata"""
        
        frame_filename = f"frame_{frame_number:06d}_{timestamp:.2f}s.jpg"
        frame_path = self.frames_dir / frame_filename
        
        cv2.imwrite(str(frame_path), frame)
        
        height, width = frame.shape[:2]
        frame_hash = hashlib.md5(frame.tobytes()).hexdigest()
        
        return {
            "frame_number": frame_number,
            "timestamp": round(timestamp, 2),
            "filename": frame_filename,
            "path": str(frame_path),
            "resolution": {"width": width, "height": height},
            "diff_score": round(diff_score, 2),
            "hash": frame_hash
        }
    
    def detect_screen_changes(self, frames_data):
        """Analyze frames to detect UI changes and actions"""
        
        print("\n🔍 Analyzing screen changes...")
        
        events = []
        
        for i, frame_info in enumerate(frames_data):
            event = {
                "event_id": i + 1,
                "timestamp": frame_info["timestamp"],
                "frame": frame_info["filename"],
                "type": "screen_change",
                "diff_score": frame_info["diff_score"]
            }
            
            if frame_info["diff_score"] > 50:
                event["change_type"] = "major"
                event["description"] = "Significant screen change detected"
            elif frame_info["diff_score"] > 30:
                event["change_type"] = "moderate"
                event["description"] = "Moderate screen change detected"
            else:
                event["change_type"] = "minor"
                event["description"] = "Minor screen change detected"
            
            events.append(event)
        
        print(f"✅ Detected {len(events)} screen change events")
        
        return events
    
    def combine_with_transcript(self, events, transcript_path):
        """Combine visual events with audio transcript"""
        
        print("\n🎤 Combining with audio transcript...")
        
        transcript_file = Path(transcript_path)
        
        if not transcript_file.exists():
            print("⚠️  Transcript file not found")
            return events
        
        with open(transcript_file, 'r') as f:
            transcript_text = f.read().strip()
        
        transcript_event = {
            "event_id": 0,
            "timestamp": 0,
            "type": "audio_transcript",
            "text": transcript_text,
            "description": "User voice commands"
        }
        
        events.insert(0, transcript_event)
        
        print(f"✅ Added transcript: {len(transcript_text)} characters")
        
        return events
    
    def generate_json_output(self, events):
        """Generate final JSON output"""
        
        session_id = self.video_path.stem
        
        output = {
            "session_id": session_id,
            "video_file": str(self.video_path),
            "processed_at": datetime.now().isoformat(),
            "total_events": len(events),
            "events": events
        }
        
        json_filename = f"{session_id}_events.json"
        json_path = self.json_dir / json_filename
        
        with open(json_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Saved JSON: {json_path}")
        
        return json_path

def process_recording(video_file, transcript_file=None):
    """Main processing function"""
    
    print("="*60)
    print("🚀 PHASE 2: VIDEO PROCESSING")
    print("="*60)
    
    processor = VideoProcessor(video_file)
    
    frames_data = processor.extract_key_frames(threshold=30, max_frames=50)
    
    events = processor.detect_screen_changes(frames_data)
    
    if transcript_file:
        events = processor.combine_with_transcript(events, transcript_file)
    
    json_path = processor.generate_json_output(events)
    
    print("\n" + "="*60)
    print("✅ PHASE 2 COMPLETE!")
    print("="*60)
    print(f"📁 Frames saved to: {processor.frames_dir}")
    print(f"📄 JSON saved to: {json_path}")
    print("="*60)
    
    return json_path

if __name__ == "__main__":
    video_dir = Path("data/video")
    transcript_dir = Path("data/transcripts")
    
    videos = sorted(video_dir.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
    transcripts = sorted(transcript_dir.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if videos:
        video_file = videos[0]
        transcript_file = transcripts[0] if transcripts else None
        
        print(f"Processing: {video_file.name}")
        if transcript_file:
            print(f"Transcript: {transcript_file.name}")
        
        process_recording(video_file, transcript_file)
    else:
        print("❌ No video files found in data/video/")
