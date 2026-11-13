import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import json

class DataManager:
    """
    Phase 5: Smart Data Management with Auto-Rotation
    Keeps only latest N recordings, automatically deletes older ones
    """
    
    def __init__(self, data_dir="data", max_recordings=5, max_storage_gb=5):
        self.data_dir = Path(data_dir)
        self.max_recordings = max_recordings
        self.max_storage_bytes = max_storage_gb * 1024 * 1024 * 1024
        self.config_file = self.data_dir / "storage_config.json"
        
        # Load or create config
        self.load_config()
    
    def load_config(self):
        """Load storage configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "max_recordings": self.max_recordings,
                "max_storage_gb": 5,
                "auto_cleanup_enabled": True,
                "last_cleanup": None,
                "total_recordings_processed": 0
            }
            self.save_config()
        
        # Update max_recordings from config
        self.max_recordings = self.config.get("max_recordings", self.max_recordings)
    
    def save_config(self):
        """Save storage configuration"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def auto_rotate_recordings(self):
        """
        Keep only the latest N recordings, delete older ones
        A 'recording session' includes: video + audio + transcript + processed data
        """
        print("\n" + "="*60)
        print("🔄 AUTO-ROTATION: Keeping Latest Recordings")
        print("="*60)
        print(f"📋 Max recordings to keep: {self.max_recordings}")
        
        # Get all sessions based on video files
        video_dir = self.data_dir / "video"
        if not video_dir.exists():
            print("⚠️  No video directory found")
            return {"deleted_sessions": 0}
        
        # Get all video files sorted by modification time (newest first)
        video_files = sorted(
            video_dir.glob("*.mp4"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if not video_files:
            print("⚠️  No recordings found")
            return {"deleted_sessions": 0}
        
        print(f"📊 Found {len(video_files)} recording sessions")
        
        # Keep only the latest N recordings
        videos_to_keep = video_files[:self.max_recordings]
        videos_to_delete = video_files[self.max_recordings:]
        
        if not videos_to_delete:
            print(f"✅ All {len(video_files)} recordings are within limit")
            return {"deleted_sessions": 0}
        
        print(f"\n🗑️  Will delete {len(videos_to_delete)} old recording(s):")
        
        deleted_sessions = 0
        total_freed = 0
        
        for video_file in videos_to_delete:
            session_name = video_file.stem
            print(f"\n   Deleting session: {session_name}")
            
            # Delete related files for this session
            freed = self.delete_session_files(session_name)
            total_freed += freed
            deleted_sessions += 1
        
        print(f"\n✅ Rotation complete!")
        print(f"   Deleted sessions: {deleted_sessions}")
        print(f"   Space freed: {self.format_size(total_freed)}")
        print(f"   Kept sessions: {len(videos_to_keep)}")
        
        # Update config
        self.config["last_cleanup"] = datetime.now().isoformat()
        self.save_config()
        
        return {
            "deleted_sessions": deleted_sessions,
            "kept_sessions": len(videos_to_keep),
            "freed_bytes": total_freed
        }
    
    def delete_session_files(self, session_name):
        """Delete all files related to a recording session"""
        freed_bytes = 0
        
        # Define file patterns to search for
        patterns = [
            ("video", f"{session_name}*.mp4"),
            ("audio", f"audio_{session_name}*.wav"),
            ("audio", f"{session_name}*.wav"),
            ("transcripts", f"{session_name}*.txt"),
            ("transcripts", f"audio_{session_name}*.txt"),
            ("processed/json", f"{session_name}*.json"),
            ("processed/frames", f"*"),  # Will filter by session
            ("screenshots", f"screenshot_{session_name}*.png")
        ]
        
        for folder, pattern in patterns:
            folder_path = self.data_dir / folder
            if not folder_path.exists():
                continue
            
            for file in folder_path.glob(pattern):
                # For frames, check if related to session
                if folder == "processed/frames":
                    if session_name not in file.name:
                        continue
                
                try:
                    size = file.stat().st_size
                    file.unlink()
                    freed_bytes += size
                    print(f"      ✅ Deleted: {file.name} ({self.format_size(size)})")
                except Exception as e:
                    print(f"      ❌ Error: {e}")
        
        return freed_bytes
    
    def get_recording_sessions(self):
        """Get list of all recording sessions with details"""
        video_dir = self.data_dir / "video"
        if not video_dir.exists():
            return []
        
        sessions = []
        video_files = sorted(
            video_dir.glob("*.mp4"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for i, video_file in enumerate(video_files, 1):
            session = {
                "number": i,
                "name": video_file.stem,
                "video_file": video_file.name,
                "video_size": video_file.stat().st_size,
                "modified": datetime.fromtimestamp(video_file.stat().st_mtime),
                "will_keep": i <= self.max_recordings
            }
            
            # Check for related files
            session["has_audio"] = self.check_related_file("audio", session["name"])
            session["has_transcript"] = self.check_related_file("transcripts", session["name"])
            session["has_processed"] = self.check_related_file("processed/json", session["name"])
            
            sessions.append(session)
        
        return sessions
    
    def check_related_file(self, folder, session_name):
        """Check if related file exists for a session"""
        folder_path = self.data_dir / folder
        if not folder_path.exists():
            return False
        
        # Check for files containing session name
        files = list(folder_path.glob(f"*{session_name}*"))
        return len(files) > 0
    
    def show_recordings_status(self):
        """Show status of all recordings with rotation info"""
        print("\n" + "="*60)
        print("📹 RECORDINGS STATUS")
        print("="*60)
        
        sessions = self.get_recording_sessions()
        
        if not sessions:
            print("\n⚠️  No recordings found")
            return
        
        print(f"\n📊 Total recordings: {len(sessions)}")
        print(f"📋 Max to keep: {self.max_recordings}")
        print(f"✅ Will keep: {sum(1 for s in sessions if s['will_keep'])}")
        print(f"🗑️  Will delete: {sum(1 for s in sessions if not s['will_keep'])}")
        
        print("\n" + "-"*60)
        print(f"{'#':<4} {'Session Name':<30} {'Size':<12} {'Status'}")
        print("-"*60)
        
        for session in sessions:
            status = "✅ KEEP" if session['will_keep'] else "🗑️  DELETE"
            size_str = self.format_size(session['video_size'])
            
            # Show completeness
            completeness = []
            if session['has_audio']:
                completeness.append("🎤")
            if session['has_transcript']:
                completeness.append("📝")
            if session['has_processed']:
                completeness.append("📊")
            
            complete_str = "".join(completeness) if completeness else "❌"
            
            print(f"{session['number']:<4} {session['name'][:28]:<30} {size_str:<12} {status} {complete_str}")
        
        print("-"*60)
        
        # Show next action
        if len(sessions) > self.max_recordings:
            print(f"\n⚠️  You have {len(sessions) - self.max_recordings} old recording(s)")
            print("💡 Run 'Auto-rotate recordings' to free up space")
        else:
            print("\n✅ Recording count is within limit")
        
        print("="*60)
    
    def get_storage_usage(self):
        """Calculate total storage used"""
        total_size = 0
        file_count = 0
        
        breakdown = {
            "audio": 0,
            "video": 0,
            "screenshots": 0,
            "processed": 0,
            "workflows": 0,
            "transcripts": 0,
            "recordings": 0
        }
        
        for folder in breakdown.keys():
            folder_path = self.data_dir / folder
            if folder_path.exists():
                for file in folder_path.rglob("*"):
                    if file.is_file():
                        size = file.stat().st_size
                        total_size += size
                        breakdown[folder] += size
                        file_count += 1
        
        return {
            "total_bytes": total_size,
            "total_mb": round(total_size / (1024 * 1024), 2),
            "total_gb": round(total_size / (1024 * 1024 * 1024), 3),
            "file_count": file_count,
            "breakdown": breakdown,
            "limit_gb": self.max_storage_bytes / (1024 * 1024 * 1024)
        }
    
    def remove_duplicate_frames(self):
        """Remove duplicate frames based on file hash"""
        print("\n🔍 Scanning for duplicate frames...")
        
        frames_dir = self.data_dir / "processed" / "frames"
        if not frames_dir.exists():
            print("   ⚠️  No frames directory found")
            return {"duplicates_removed": 0}
        
        seen_hashes = {}
        duplicates = []
        freed_bytes = 0
        
        for frame in frames_dir.glob("*.jpg"):
            file_hash = self.calculate_file_hash(frame)
            
            if file_hash in seen_hashes:
                size = frame.stat().st_size
                duplicates.append(str(frame))
                freed_bytes += size
                
                try:
                    frame.unlink()
                    print(f"   ✅ Removed duplicate: {frame.name} ({self.format_size(size)})")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
            else:
                seen_hashes[file_hash] = str(frame)
        
        print(f"\n✅ Removed {len(duplicates)} duplicates, freed {self.format_size(freed_bytes)}")
        
        return {
            "duplicates_removed": len(duplicates),
            "freed_bytes": freed_bytes
        }
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def format_size(self, bytes_size):
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    def show_storage_report(self):
        """Display detailed storage usage report"""
        usage = self.get_storage_usage()
        
        print("\n" + "="*60)
        print("📊 STORAGE USAGE REPORT")
        print("="*60)
        
        print(f"\n💾 Total Storage: {usage['total_gb']:.3f} GB")
        print(f"📁 Total Files: {usage['file_count']}")
        
        # Breakdown
        print("\n📂 Breakdown by folder:")
        sorted_breakdown = sorted(usage['breakdown'].items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)
        
        for folder, size in sorted_breakdown:
            if size > 0:
                size_str = self.format_size(size)
                print(f"   {folder:15s}: {size_str:>12s}")
        
        print("="*60)
        
        return usage

def main():
    """Main menu for data management"""
    
    manager = DataManager(max_recordings=5)
    
    while True:
        print("\n" + "="*60)
        print("💾 SMART DATA MANAGEMENT - AUTO-ROTATION")
        print("="*60)
        print(f"⚙️  Current: Keep latest {manager.max_recordings} recordings")
        print("\n1. Show recordings status")
        print("2. Auto-rotate recordings (delete old)")
        print("3. Show storage report")
        print("4. Remove duplicate frames")
        print("5. Change max recordings limit")
        print("6. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            manager.show_recordings_status()
        
        elif choice == '2':
            confirm = input(f"\n⚠️  Delete recordings older than latest {manager.max_recordings}? (yes/no): ")
            if confirm.lower() == 'yes':
                manager.auto_rotate_recordings()
            else:
                print("❌ Cancelled")
        
        elif choice == '3':
            manager.show_storage_report()
        
        elif choice == '4':
            manager.remove_duplicate_frames()
        
        elif choice == '5':
            print(f"\n⚙️  Current limit: {manager.max_recordings} recordings")
            try:
                new_limit = int(input("New limit (5-10 recommended): "))
                if 1 <= new_limit <= 50:
                    manager.max_recordings = new_limit
                    manager.config['max_recordings'] = new_limit
                    manager.save_config()
                    print(f"✅ Updated to keep {new_limit} recordings")
                else:
                    print("❌ Please enter a number between 1 and 50")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()