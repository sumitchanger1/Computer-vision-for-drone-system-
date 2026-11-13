"""
Smart File Organizer AI - Command Line Version
Automatically organizes files with intelligent pattern recognition
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import mimetypes
import re

# Color codes for terminal (works on Windows/Mac/Linux)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SmartFileOrganizer:
    def __init__(self, source_folder=None):
        self.source_folder = source_folder or str(Path.home() / "Downloads")
        self.stats = {
            'total_files': 0,
            'organized': 0,
            'time_saved': 0,
            'categories': {}
        }
        self.reasoning_log = []
        
        # File categorization rules
        self.categories = {
            'Documents/Work': {
                'extensions': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx'],
                'keywords': ['report', 'presentation', 'meeting', 'project', 'proposal']
            },
            'Documents/Finance': {
                'extensions': ['.pdf', '.xlsx', '.csv'],
                'keywords': ['invoice', 'receipt', 'bill', 'payment', 'tax', 'statement']
            },
            'Pictures/Personal': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
                'keywords': ['photo', 'picture', 'image', 'vacation', 'family', 'selfie']
            },
            'Pictures/Screenshots': {
                'extensions': ['.png', '.jpg'],
                'keywords': ['screenshot', 'screen', 'capture', 'snap']
            },
            'Music/Playlists': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                'keywords': ['song', 'music', 'audio', 'playlist', 'podcast']
            },
            'Videos/Tutorials': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
                'keywords': ['video', 'tutorial', 'movie', 'clip', 'recording']
            },
            'Archives/Backups': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'keywords': ['backup', 'archive', 'compressed', 'package']
            },
            'Code/Projects': {
                'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.json'],
                'keywords': ['code', 'script', 'program', 'project', 'source']
            }
        }

    def print_header(self):
        """Print fancy header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}🤖  SMART FILE ORGANIZER AI - v1.0{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
        print(f"{Colors.YELLOW}📁 Source Folder: {Colors.END}{self.source_folder}")
        print(f"{Colors.YELLOW}🧠 AI Engine: {Colors.END}{Colors.GREEN}LOADED ✓{Colors.END}\n")

    def analyze_file(self, filename):
        """AI analysis of file to determine best category"""
        file_lower = filename.lower()
        _, ext = os.path.splitext(filename)
        
        scores = {}
        reasoning = []
        
        # Score each category
        for category, rules in self.categories.items():
            score = 0
            reasons = []
            
            # Check extension match
            if ext.lower() in rules['extensions']:
                score += 10
                reasons.append(f"Extension '{ext}' matches category")
            
            # Check keyword match
            for keyword in rules['keywords']:
                if keyword in file_lower:
                    score += 5
                    reasons.append(f"Keyword '{keyword}' found in filename")
            
            if score > 0:
                scores[category] = score
                reasoning.append((category, reasons, score))
        
        # Get best category or default
        if scores:
            best_category = max(scores, key=scores.get)
            best_reasons = [r for c, r, s in reasoning if c == best_category][0]
            return best_category, best_reasons, scores[best_category]
        else:
            return 'Others/Miscellaneous', ['No specific pattern detected'], 0

    def get_file_info(self, filepath):
        """Get detailed file information"""
        stat = os.stat(filepath)
        size = stat.st_size
        
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
        
        return {
            'size': size_str,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }

    def organize_files(self, dry_run=False):
        """Main organization function"""
        self.print_header()
        
        print(f"{Colors.BLUE}🔍 Scanning folder...{Colors.END}\n")
        time.sleep(1)
        
        # Get all files
        try:
            files = [f for f in os.listdir(self.source_folder) 
                    if os.path.isfile(os.path.join(self.source_folder, f))]
        except Exception as e:
            print(f"{Colors.RED}❌ Error accessing folder: {e}{Colors.END}")
            return
        
        if not files:
            print(f"{Colors.YELLOW}⚠️  No files found to organize{Colors.END}")
            return
        
        self.stats['total_files'] = len(files)
        print(f"{Colors.GREEN}✓ Found {len(files)} files to organize{Colors.END}\n")
        time.sleep(1)
        
        # Process each file
        for idx, filename in enumerate(files, 1):
            filepath = os.path.join(self.source_folder, filename)
            
            # Skip if it's a directory or hidden file
            if not os.path.isfile(filepath) or filename.startswith('.'):
                continue
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{Colors.CYAN}[{timestamp}] 📄 {filename}{Colors.END}")
            
            # Get file info
            file_info = self.get_file_info(filepath)
            print(f"           {Colors.YELLOW}├─ Size: {file_info['size']}{Colors.END}")
            
            # AI Analysis
            print(f"           {Colors.YELLOW}├─ 🧠 Analyzing...{Colors.END}")
            time.sleep(0.5)  # Simulate AI thinking
            
            category, reasons, confidence = self.analyze_file(filename)
            
            # Print reasoning
            for reason in reasons:
                print(f"           {Colors.YELLOW}│  • {reason}{Colors.END}")
            
            print(f"           {Colors.YELLOW}├─ Confidence: {confidence}/10{Colors.END}")
            print(f"           {Colors.YELLOW}├─ Destination: {Colors.BOLD}{category}{Colors.END}")
            
            # Move file
            if not dry_run:
                try:
                    # Create destination folder if needed
                    dest_folder = os.path.join(self.source_folder, category)
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    # Move file
                    dest_path = os.path.join(dest_folder, filename)
                    
                    # Handle duplicate names
                    if os.path.exists(dest_path):
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(dest_path):
                            new_name = f"{base}_{counter}{ext}"
                            dest_path = os.path.join(dest_folder, new_name)
                            counter += 1
                    
                    shutil.move(filepath, dest_path)
                    
                    print(f"           {Colors.GREEN}└─ ✅ Moved successfully{Colors.END}\n")
                    
                    self.stats['organized'] += 1
                    self.stats['time_saved'] += 2.5  # 2.5 min per file
                    
                    if category not in self.stats['categories']:
                        self.stats['categories'][category] = 0
                    self.stats['categories'][category] += 1
                    
                    # Log reasoning
                    self.reasoning_log.append({
                        'file': filename,
                        'category': category,
                        'reasons': reasons,
                        'confidence': confidence,
                        'timestamp': timestamp
                    })
                    
                except Exception as e:
                    print(f"           {Colors.RED}└─ ❌ Error: {e}{Colors.END}\n")
            else:
                print(f"           {Colors.BLUE}└─ 🔍 DRY RUN - No files moved{Colors.END}\n")
                self.stats['organized'] += 1
            
            time.sleep(0.3)  # Small delay for readability
        
        # Print summary
        self.print_summary()
        
        # Generate report
        if not dry_run:
            self.generate_report()

    def print_summary(self):
        """Print organization summary"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}✅ ORGANIZATION COMPLETE!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
        
        print(f"{Colors.CYAN}📊 Statistics:{Colors.END}")
        print(f"   • Files organized: {Colors.BOLD}{self.stats['organized']}/{self.stats['total_files']}{Colors.END}")
        print(f"   • Time saved: {Colors.BOLD}{self.stats['time_saved']:.1f} minutes{Colors.END}")
        print(f"   • Categories used: {Colors.BOLD}{len(self.stats['categories'])}{Colors.END}\n")
        
        if self.stats['categories']:
            print(f"{Colors.CYAN}📂 Files per Category:{Colors.END}")
            for category, count in sorted(self.stats['categories'].items(), key=lambda x: x[1], reverse=True):
                bar = '█' * count
                print(f"   {category:30s} {Colors.GREEN}{bar}{Colors.END} ({count})")
        
        print()

    def generate_report(self):
        """Generate detailed report file"""
        report_name = f"organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = os.path.join(self.source_folder, report_name)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("SMART FILE ORGANIZER AI - ORGANIZATION REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source Folder: {self.source_folder}\n\n")
            
            f.write("SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Files: {self.stats['total_files']}\n")
            f.write(f"Organized: {self.stats['organized']}\n")
            f.write(f"Time Saved: {self.stats['time_saved']:.1f} minutes\n")
            f.write(f"Categories: {len(self.stats['categories'])}\n\n")
            
            f.write("DETAILED LOG\n")
            f.write("-"*70 + "\n\n")
            
            for entry in self.reasoning_log:
                f.write(f"[{entry['timestamp']}] {entry['file']}\n")
                f.write(f"  Category: {entry['category']}\n")
                f.write(f"  Confidence: {entry['confidence']}/10\n")
                f.write(f"  Reasoning:\n")
                for reason in entry['reasons']:
                    f.write(f"    • {reason}\n")
                f.write("\n")
            
            f.write("="*70 + "\n")
            f.write("Report generated by Smart File Organizer AI\n")
        
        print(f"{Colors.YELLOW}📄 Report saved: {Colors.BOLD}{report_name}{Colors.END}\n")


def main():
    """Main function"""
    print(f"\n{Colors.BOLD}Welcome to Smart File Organizer AI!{Colors.END}\n")
    
    # Get source folder
    default_path = str(Path.home() / "Downloads")
    print(f"Default folder: {Colors.CYAN}{default_path}{Colors.END}")
    user_path = input(f"Enter folder path (or press Enter for default): ").strip()
    
    source = user_path if user_path else default_path
    
    if not os.path.exists(source):
        print(f"{Colors.RED}❌ Folder does not exist!{Colors.END}")
        return
    
    # Ask for dry run
    dry_run_input = input(f"\nDry run? (preview without moving files) [y/N]: ").strip().lower()
    dry_run = dry_run_input == 'y'
    
    # Confirm
    if not dry_run:
        confirm = input(f"\n{Colors.YELLOW}⚠️  Files will be moved. Continue? [y/N]: {Colors.END}").strip().lower()
        if confirm != 'y':
            print(f"{Colors.RED}Operation cancelled.{Colors.END}")
            return
    
    # Run organizer
    organizer = SmartFileOrganizer(source)
    organizer.organize_files(dry_run=dry_run)
    
    print(f"{Colors.GREEN}Thank you for using Smart File Organizer AI! 🚀{Colors.END}\n")


if __name__ == "__main__":
    main()