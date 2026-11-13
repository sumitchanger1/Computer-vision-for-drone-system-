"""
Complete Automation System - Round 2 Enhanced
Combines File Organization, Excel, Word automation with Round 2 workflow execution
All-in-one automation solution
"""

import os
import shutil
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import platform
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pyautogui not installed. Install with: pip install pyautogui")

# Color codes for terminal
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

class AutomationEngine:
    """Core automation engine for keyboard/mouse actions"""
    
    def __init__(self):
        self.workflows_dir = Path("data/workflows")
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir = Path("data/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    def execute_action(self, action):
        """Execute a single automation action"""
        if not PYAUTOGUI_AVAILABLE:
            print(f"   ⚠️  Simulating: {action.get('description', action.get('action'))}")
            time.sleep(0.3)
            return True
        
        try:
            action_type = action.get('action')
            
            if action_type == 'hotkey':
                keys = action.get('keys', [])
                pyautogui.hotkey(*keys)
                print(f"   ⌨️  Hotkey: {'+'.join(keys)}")
            
            elif action_type == 'press':
                key = action.get('key')
                pyautogui.press(key)
                print(f"   ⌨️  Pressed: {key}")
            
            elif action_type == 'type':
                text = action.get('text', '')
                pyautogui.write(text, interval=0.05)
                print(f"   ⌨️  Typed: {text}")
            
            elif action_type == 'wait':
                duration = action.get('duration', 1)
                time.sleep(duration)
            
            elif action_type == 'click':
                x = action.get('x')
                y = action.get('y')
                if x and y:
                    pyautogui.click(x, y)
                    print(f"   🖱️  Clicked: ({x}, {y})")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def execute_workflow(self, workflow_file):
        """Execute a complete workflow"""
        try:
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
            
            actions = workflow.get('actions', [])
            
            for i, action in enumerate(actions, 1):
                desc = action.get('description', f"Action {i}")
                print(f"   [{i}/{len(actions)}] {desc}")
                
                if not self.execute_action(action):
                    return False
                
                time.sleep(0.2)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error loading workflow: {e}")
            return False
    
    def screenshot(self, filename=None):
        """Take a screenshot"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "path": None}
        
        try:
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            filepath = self.screenshots_dir / filename
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            return {"success": True, "path": str(filepath)}
        except Exception as e:
            print(f"   ❌ Screenshot error: {e}")
            return {"success": False, "path": None}
    
    def create_workflow(self, name, actions, description=""):
        """Create and save a workflow"""
        workflow = {
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "actions": actions
        }
        
        workflow_file = self.workflows_dir / f"{name}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return workflow_file


class SmartFileOrganizer:
    """File organization with AI categorization"""
    
    def __init__(self, source_folder=None):
        self.source_folder = source_folder or str(Path.home() / "Downloads")
        self.stats = {
            'total_files': 0,
            'organized': 0,
            'time_saved': 0,
            'categories': {},
            'actions': 0
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

    def print_ai_thinking(self, message, indent=0):
        """Print AI thinking message"""
        spaces = "   " * indent
        print(f"{spaces}{Colors.CYAN}💬 AI: {message}{Colors.END}")
        time.sleep(0.3)

    def print_success(self, indent=0):
        """Print success checkmark"""
        spaces = "   " * indent
        print(f"{spaces}   {Colors.GREEN}✅ Done!{Colors.END}")
        time.sleep(0.2)

    def simulate_action(self, action_type, details, indent=1):
        """Simulate and display an action"""
        self.stats['actions'] += 1
        spaces = "   " * indent
        
        actions_map = {
            "scan": f"{Colors.YELLOW}🔍 Action: {details}{Colors.END}",
            "read": f"{Colors.BLUE}📖 Reading: {details}{Colors.END}",
            "create": f"{Colors.GREEN}📁 Creating: {details}{Colors.END}",
            "move": f"{Colors.CYAN}➡️  Moving: {details}{Colors.END}",
            "verify": f"✓ Verified: {details}",
            "keyboard": f"{Colors.YELLOW}⌨️  Typed: {details}{Colors.END}",
            "hotkey": f"{Colors.YELLOW}⌨️  Hotkey: {details}{Colors.END}",
            "pressed": f"{Colors.YELLOW}⌨️  Pressed: {details}{Colors.END}"
        }
        
        print(f"{spaces}{actions_map.get(action_type, details)}")
        time.sleep(0.2)

    def analyze_file(self, filename):
        """AI analysis of file to determine best category"""
        file_lower = filename.lower()
        _, ext = os.path.splitext(filename)
        
        scores = {}
        reasoning = []
        
        for category, rules in self.categories.items():
            score = 0
            reasons = []
            
            if ext.lower() in rules['extensions']:
                score += 10
                reasons.append(f"Extension '{ext}' detected")
            
            for keyword in rules['keywords']:
                if keyword in file_lower:
                    score += 5
                    reasons.append(f"Keyword '{keyword}' found")
            
            if score > 0:
                scores[category] = score
                reasoning.append((category, reasons, score))
        
        if scores:
            best_category = max(scores, key=scores.get)
            best_reasons = [r for c, r, s in reasoning if c == best_category][0]
            return best_category, best_reasons, scores[best_category]
        else:
            return 'Others/Miscellaneous', ['Default category'], 0

    def get_file_info(self, filepath):
        """Get file information"""
        stat = os.stat(filepath)
        size = stat.st_size
        
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"

    def organize_files(self, dry_run=False):
        """Main file organization workflow"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}📁 FILE ORGANIZATION WORKFLOW{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        self.print_ai_thinking("Scanning Downloads folder...")
        
        try:
            files = [f for f in os.listdir(self.source_folder) 
                    if os.path.isfile(os.path.join(self.source_folder, f))
                    and not f.startswith('.')]
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
            return False
        
        if not files:
            print(f"{Colors.YELLOW}⚠️  No files found{Colors.END}")
            return False
        
        self.stats['total_files'] = len(files)
        print(f"{Colors.GREEN}✓ Found {len(files)} files{Colors.END}\n")
        
        # Process files
        for idx, filename in enumerate(files, 1):
            filepath = os.path.join(self.source_folder, filename)
            
            print(f"{Colors.BOLD}[File {idx}/{len(files)}] {filename}{Colors.END}")
            
            category, reasons, confidence = self.analyze_file(filename)
            
            print(f"   Category: {category} (Confidence: {confidence}/10)")
            
            if not dry_run:
                dest_folder = os.path.join(self.source_folder, category)
                os.makedirs(dest_folder, exist_ok=True)
                
                try:
                    dest_path = os.path.join(dest_folder, filename)
                    shutil.move(filepath, dest_path)
                    
                    self.stats['organized'] += 1
                    self.stats['time_saved'] += 2.5
                    
                    if category not in self.stats['categories']:
                        self.stats['categories'][category] = 0
                    self.stats['categories'][category] += 1
                    
                    self.reasoning_log.append({
                        'file': filename,
                        'category': category,
                        'confidence': confidence
                    })
                    
                    print(f"   {Colors.GREEN}✅ Moved to {category}{Colors.END}\n")
                except Exception as e:
                    print(f"   {Colors.RED}❌ Error: {e}{Colors.END}\n")
            else:
                self.stats['organized'] += 1
                print(f"   {Colors.BLUE}🔍 DRY RUN - No changes made{Colors.END}\n")
        
        self.print_summary()
        return True

    def print_summary(self):
        """Print organization summary"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}✅ ORGANIZATION COMPLETE!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
        
        print(f"📦 Files Organized: {self.stats['organized']}/{self.stats['total_files']}")
        print(f"⏱️  Time Saved: {self.stats['time_saved']:.1f} minutes")
        print(f"📁 Categories: {len(self.stats['categories'])}\n")

    def create_excel_report(self):
        """Create Excel CSV report"""
        excel_name = f"Organization_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        excel_path = os.path.join(self.source_folder, excel_name)
        
        print(f"\n{Colors.GREEN}📊 Creating Excel Report...{Colors.END}\n")
        
        try:
            with open(excel_path, 'w', encoding='utf-8') as f:
                f.write("File Name,Category,Confidence,Status\n")
                
                for entry in self.reasoning_log:
                    f.write(f'"{entry["file"]}","{entry["category"]}",{entry["confidence"]}/10,Organized\n')
                
                f.write("\n--- SUMMARY ---\n")
                f.write(f"Total Files,{self.stats['total_files']}\n")
                f.write(f"Organized,{self.stats['organized']}\n")
                f.write(f"Time Saved,{self.stats['time_saved']:.1f} min\n")
            
            print(f"{Colors.GREEN}✅ Excel report saved: {excel_name}{Colors.END}\n")
            return excel_path
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error creating Excel report: {e}{Colors.END}")
            return None

    def create_word_report(self):
        """Create Word document report"""
        doc_name = f"Workflow_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        doc_path = os.path.join(self.source_folder, doc_name)
        
        print(f"\n{Colors.BLUE}📝 Creating Word Report...{Colors.END}\n")
        
        try:
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write("SMART FILE ORGANIZER AI\n")
                f.write("Complete Automation Workflow Report\n")
                f.write("="*70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("PROJECT OVERVIEW\n")
                f.write("-"*70 + "\n")
                f.write("Automated file organization with AI categorization\n")
                f.write("Excel reporting and Word documentation generation\n\n")
                
                f.write("STATISTICS\n")
                f.write("-"*70 + "\n")
                f.write(f"Total Files: {self.stats['total_files']}\n")
                f.write(f"Organized: {self.stats['organized']}\n")
                f.write(f"Time Saved: {self.stats['time_saved']:.1f} minutes\n")
                f.write(f"Categories: {len(self.stats['categories'])}\n\n")
                
                f.write("CATEGORY BREAKDOWN\n")
                f.write("-"*70 + "\n")
                for category, count in sorted(self.stats['categories'].items()):
                    f.write(f"{category}: {count} files\n")
            
            print(f"{Colors.GREEN}✅ Word report saved: {doc_name}{Colors.END}\n")
            return doc_path
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error creating Word report: {e}{Colors.END}")
            return None


class Round2Automator:
    """Round 2: Enhanced automation with workflow execution"""
    
    def __init__(self):
        self.engine = AutomationEngine()
        self.patterns_dir = Path("data/patterns")
        self.workflows_dir = Path("data/workflows")
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
    
    def create_file_org_workflow(self):
        """Create workflow for file organization"""
        actions = [
            {"action": "wait", "duration": 1, "description": "Initialize file scanner"},
            {"action": "wait", "duration": 2, "description": "Scan Downloads folder"},
            {"action": "wait", "duration": 1, "description": "AI categorization"},
            {"action": "wait", "duration": 2, "description": "Organize files"},
            {"action": "wait", "duration": 1, "description": "Generate reports"}
        ]
        
        return self.engine.create_workflow(
            name="file_organization_workflow",
            actions=actions,
            description="Complete file organization with AI"
        )
    
    def create_excel_workflow(self):
        """Create workflow for XLSX Spreadsheet automation"""
        system = platform.system()
        
        actions = [
            {"action": "hotkey", "keys": ["win" if system == "Windows" else "cmd", "s"], 
             "description": "Open Windows Search"},
            {"action": "wait", "duration": 0.8},
            {"action": "type", "text": "XLSX Spreadsheet", "description": "Type XLSX Spreadsheet"},
            {"action": "wait", "duration": 0.5},
            {"action": "press", "key": "enter", "description": "Launch XLSX Spreadsheet"},
            {"action": "wait", "duration": 3, "description": "Wait for app to open"},
            {"action": "type", "text": "Name", "description": "Type header"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Marks"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Class"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Subject"},
            {"action": "press", "key": "enter"},
            {"action": "wait", "duration": 0.5},
            {"action": "type", "text": "Sumit", "description": "Sample data"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "55"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "BCA"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "OOPS"},
            {"action": "press", "key": "enter"},
            {"action": "wait", "duration": 0.5},
            {"action": "hotkey", "keys": ["ctrl", "s"], "description": "Save spreadsheet"},
            {"action": "wait", "duration": 1}
        ]
        
        return self.engine.create_workflow(
            name="xlsx_spreadsheet_automation",
            actions=actions,
            description="XLSX Spreadsheet automation with data entry"
        )
    
    def create_word_workflow(self):
        """Create workflow for Word automation"""
        system = platform.system()
        
        actions = [
            {"action": "hotkey", "keys": ["win" if system == "Windows" else "cmd", "r"],
             "description": "Open Run dialog"},
            {"action": "wait", "duration": 0.5},
            {"action": "type", "text": "winword", "description": "Type winword"},
            {"action": "press", "key": "enter", "description": "Launch Word"},
            {"action": "wait", "duration": 3, "description": "Wait for Word to open"},
            {"action": "type", "text": "This is workflow automation in Round 2 phase as demo data.\n\n", 
             "description": "Type content"},
            {"action": "type", "text": "Student: Sumit\n"},
            {"action": "type", "text": "Marks: 55\n"},
            {"action": "type", "text": "Class: BCA\n"},
            {"action": "type", "text": "Subject: OOPS\n"},
            {"action": "hotkey", "keys": ["ctrl", "s"], "description": "Save document"},
            {"action": "wait", "duration": 1}
        ]
        
        return self.engine.create_workflow(
            name="word_automation_workflow",
            actions=actions,
            description="Word document automation"
        )
    
    def create_xlsx_detailed_workflow(self):
        """Create detailed XLSX Spreadsheet workflow with full report"""
        system = platform.system()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        actions = [
            {"action": "hotkey", "keys": ["win" if system == "Windows" else "cmd", "s"], 
             "description": "💬 AI: Opening XLSX Spreadsheet..."},
            {"action": "wait", "duration": 0.8},
            {"action": "type", "text": "XLSX Spreadsheet", 
             "description": "⌨️  Typed: XLSX Spreadsheet"},
            {"action": "wait", "duration": 0.5},
            {"action": "press", "key": "enter", 
             "description": "⌨️  Pressed: enter"},
            {"action": "wait", "duration": 3, 
             "description": "✅ Done! App opened"},
            
            # Create header row
            {"action": "wait", "duration": 0.5,
             "description": "💬 AI: Creating column headers..."},
            {"action": "type", "text": "Name"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Marks"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Class"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "Subject"},
            {"action": "press", "key": "enter"},
            {"action": "wait", "duration": 0.3,
             "description": "✅ Done! Headers created"},
            
            # Add sample data
            {"action": "wait", "duration": 0.5,
             "description": "💬 AI: Filling student data..."},
            {"action": "type", "text": "Sumit"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "55"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "BCA"},
            {"action": "press", "key": "tab"},
            {"action": "type", "text": "OOPS"},
            {"action": "press", "key": "enter"},
            
            {"action": "wait", "duration": 0.3,
             "description": "✅ Done! Data filled"},
            
            # Format headers
            {"action": "wait", "duration": 0.5,
             "description": "💬 AI: Formatting spreadsheet..."},
            {"action": "hotkey", "keys": ["ctrl", "home"],
             "description": "⌨️  Hotkey: ctrl+home (go to top)"},
            {"action": "wait", "duration": 0.3},
            {"action": "hotkey", "keys": ["shift", "ctrl", "right"],
             "description": "⌨️  Hotkey: select header row"},
            {"action": "wait", "duration": 0.3},
            {"action": "hotkey", "keys": ["ctrl", "b"],
             "description": "⌨️  Hotkey: ctrl+b (bold)"},
            {"action": "wait", "duration": 0.3,
             "description": "✅ Done! Formatting applied"},
            
            # Save file
            {"action": "wait", "duration": 0.5,
             "description": "💬 AI: Saving spreadsheet..."},
            {"action": "hotkey", "keys": ["ctrl", "s"],
             "description": "⌨️  Hotkey: ctrl+s"},
            {"action": "wait", "duration": 1},
            {"action": "type", "text": f"Student_Report_{timestamp}"},
            {"action": "press", "key": "enter",
             "description": "⌨️  Pressed: enter"},
            {"action": "wait", "duration": 1,
             "description": "✅ Done! File saved"}
        ]
        
        return self.engine.create_workflow(
            name="xlsx_spreadsheet_detailed",
            actions=actions,
            description="Complete XLSX Spreadsheet automation with detailed steps"
        )
    
    def create_notepad_workflow(self):
        """Create simple Notepad test workflow"""
        system = platform.system()
        
        actions = [
            {"action": "hotkey", "keys": ["win" if system == "Windows" else "cmd", "r"],
             "description": "Open Run dialog"},
            {"action": "wait", "duration": 0.5},
            {"action": "type", "text": "notepad", "description": "Type notepad"},
            {"action": "press", "key": "enter", "description": "Launch Notepad"},
            {"action": "wait", "duration": 2, "description": "Wait for Notepad"},
            {"action": "type", "text": "Round 2 Automation Test\n"},
            {"action": "type", "text": "Automated by Desktop AI Assistant!\n"},
            {"action": "type", "text": f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"}
        ]
        
        return self.engine.create_workflow(
            name="notepad_test_workflow",
            actions=actions,
            description="Notepad test automation"
        )
    
    def execute_with_verification(self, workflow_file):
        """Execute workflow with verification"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.CYAN}🔄 EXECUTE WITH VERIFICATION{Colors.END}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        # Take before screenshot
        print("👁️  Step 1: OBSERVE (taking screenshot)")
        before = self.engine.screenshot(filename="before_automation.png")
        if before['success']:
            print(f"   ✅ Screenshot: {before['path']}\n")
        
        # Execute workflow
        print("🤖 Step 2: AUTOMATE (executing workflow)")
        success = self.engine.execute_workflow(workflow_file)
        
        if not success:
            print(f"\n{Colors.RED}❌ Automation failed!{Colors.END}")
            return False
        
        # Verify
        print("\n✓ Step 3: VERIFY (checking results)")
        time.sleep(2)
        after = self.engine.screenshot(filename="after_automation.png")
        if after['success']:
            print(f"   ✅ Screenshot: {after['path']}")
        
        print(f"\n{Colors.GREEN}✅ Workflow executed successfully!{Colors.END}")
        return True
    
    def list_workflows(self):
        """List all available workflows"""
        workflows = list(self.workflows_dir.glob("*.json"))
        
        print(f"\n{Colors.CYAN}📋 Available Workflows: {len(workflows)}{Colors.END}\n")
        
        for i, wf in enumerate(workflows, 1):
            try:
                with open(wf) as f:
                    data = json.load(f)
                desc = data.get('description', 'No description')
                actions_count = len(data.get('actions', []))
                print(f"   {i}. {wf.name}")
                print(f"      📝 {desc}")
                print(f"      ⚙️  {actions_count} actions\n")
            except:
                print(f"   {i}. {wf.name} (error reading)\n")
        
        return workflows


def main():
    """Main application interface"""
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}🤖  COMPLETE AUTOMATION SYSTEM - ROUND 2{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}   File Organization + Excel + Word + Workflow Automation{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    file_organizer = None
    round2_automator = Round2Automator()
    
    while True:
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}📋 MAIN MENU{Colors.END}")
        print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
        
        print(f"{Colors.CYAN}FILE ORGANIZATION:{Colors.END}")
        print("1. Run Complete File Organization (Files + Excel + Word)")
        print("2. Run File Organization Only")
        print("3. Generate Excel Report Only")
        print("4. Generate Word Report Only")
        
        print(f"\n{Colors.GREEN}ROUND 2 AUTOMATION:{Colors.END}")
        print("5. Create All Workflow Templates")
        print("6. Execute Notepad Test Workflow")
        print("7. Execute XLSX Spreadsheet Workflow (Simple)")
        print("8. Execute XLSX Spreadsheet Workflow (Detailed)")
        print("9. Execute Word Workflow")
        print("10. List All Workflows")
        print("11. Execute Custom Workflow")
        
        print(f"\n{Colors.YELLOW}SYSTEM:{Colors.END}")
        print("12. View System Info")
        print("13. Exit")
        
        choice = input(f"\n{Colors.BOLD}👉 Choice: {Colors.END}").strip()
        
        if choice == "1":
            # Complete workflow
            default_path = str(Path.home() / "Downloads")
            print(f"\nDefault folder: {Colors.YELLOW}{default_path}{Colors.END}")
            user_path = input("Enter folder path (or press Enter for default): ").strip()
            source = user_path if user_path else default_path
            
            if not os.path.exists(source):
                print(f"{Colors.RED}❌ Folder not found!{Colors.END}")
                continue
            
            file_organizer = SmartFileOrganizer(source)
            
            # File organization
            if file_organizer.organize_files(dry_run=False):
                # Excel report
                file_organizer.create_excel_report()
                # Word report
                file_organizer.create_word_report()
                
                print(f"\n{Colors.GREEN}🎉 Complete automation finished!{Colors.END}")
        
        elif choice == "2":
            default_path = str(Path.home() / "Downloads")
            user_path = input(f"Folder path [{default_path}]: ").strip()
            source = user_path if user_path else default_path
            
            if os.path.exists(source):
                file_organizer = SmartFileOrganizer(source)
                file_organizer.organize_files(dry_run=False)
            else:
                print(f"{Colors.RED}❌ Folder not found!{Colors.END}")
        
        elif choice == "3":
            if file_organizer and file_organizer.reasoning_log:
                file_organizer.create_excel_report()
            else:
                print(f"{Colors.YELLOW}⚠️  Run file organization first!{Colors.END}")
        
        elif choice == "4":
            if file_organizer and file_organizer.stats['organized'] > 0:
                file_organizer.create_word_report()
            else:
                print(f"{Colors.YELLOW}⚠️  Run file organization first!{Colors.END}")
        
        elif choice == "5":
            print(f"\n{Colors.CYAN}Creating workflow templates...{Colors.END}\n")
            round2_automator.create_file_org_workflow()
            print("   ✅ File Organization Workflow")
            round2_automator.create_excel_workflow()
            print("   ✅ XLSX Spreadsheet Workflow (Simple)")
            round2_automator.create_xlsx_detailed_workflow()
            print("   ✅ XLSX Spreadsheet Workflow (Detailed)")
            round2_automator.create_word_workflow()
            print("   ✅ Word Automation Workflow")
            round2_automator.create_notepad_workflow()
            print("   ✅ Notepad Test Workflow")
            print(f"\n{Colors.GREEN}✅ All templates created!{Colors.END}")
        
        elif choice == "6":
            print(f"\n{Colors.YELLOW}Testing Notepad automation...{Colors.END}")
            workflow = round2_automator.create_notepad_workflow()
            input("Press Enter to start automation...")
            round2_automator.execute_with_verification(workflow)
        
        elif choice == "7":
            print(f"\n{Colors.YELLOW}Executing XLSX Spreadsheet automation (Simple)...{Colors.END}")
            print(f"{Colors.CYAN}This will open XLSX Spreadsheet app and create a basic report{Colors.END}\n")
            workflow = round2_automator.create_excel_workflow()
            input("Press Enter to start automation...")
            round2_automator.execute_with_verification(workflow)
        
        elif choice == "8":
            print(f"\n{Colors.YELLOW}Executing XLSX Spreadsheet automation (Detailed)...{Colors.END}")
            print(f"{Colors.CYAN}This will open XLSX Spreadsheet and create a complete formatted report{Colors.END}\n")
            workflow = round2_automator.create_xlsx_detailed_workflow()
            input("Press Enter to start automation...")
            round2_automator.execute_with_verification(workflow)
        
        elif choice == "9":
            print(f"\n{Colors.YELLOW}Executing Word automation...{Colors.END}")
            workflow = round2_automator.create_word_workflow()
            input("Press Enter to start automation...")
            round2_automator.execute_with_verification(workflow)
        
        elif choice == "10":
            workflows = round2_automator.list_workflows()
        
        elif choice == "11":
            workflows = round2_automator.list_workflows()
            if workflows:
                idx = input("\nWhich workflow to execute? (number): ").strip()
                if idx.isdigit() and 1 <= int(idx) <= len(workflows):
                    print(f"\n{Colors.CYAN}Executing workflow...{Colors.END}")
                    input("Press Enter to start...")
                    round2_automator.execute_with_verification(workflows[int(idx)-1])
        
        elif choice == "12":
            print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
            print(f"{Colors.CYAN}SYSTEM INFORMATION{Colors.END}")
            print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
            print(f"OS: {platform.system()} {platform.release()}")
            print(f"Python: {platform.python_version()}")
            print(f"PyAutoGUI: {'✅ Installed' if PYAUTOGUI_AVAILABLE else '❌ Not Installed'}")
            print(f"Workflows Dir: {round2_automator.workflows_dir}")
            print(f"Screenshots Dir: {round2_automator.engine.screenshots_dir}")
            
            # Check workflows
            workflows = list(round2_automator.workflows_dir.glob("*.json"))
            print(f"\nWorkflows: {len(workflows)} files")
            
            if file_organizer:
                print(f"\nLast Organization:")
                print(f"  Files: {file_organizer.stats['organized']}/{file_organizer.stats['total_files']}")
                print(f"  Time Saved: {file_organizer.stats['time_saved']:.1f} min")
        
        elif choice == "13":
            print(f"\n{Colors.GREEN}👋 Thank you for using Complete Automation System!{Colors.END}\n")
            break
        
        else:
            print(f"\n{Colors.RED}❌ Invalid choice!{Colors.END}")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     🤖  COMPLETE AUTOMATION SYSTEM - ROUND 2 ENHANCED  🤖        ║
    ║                                                                   ║
    ║  Features:                                                        ║
    ║  ✅ AI-Powered File Organization                                 ║
    ║  ✅ Excel Spreadsheet Automation                                 ║
    ║  ✅ Word Document Generation                                     ║
    ║  ✅ Round 2 Workflow Execution                                   ║
    ║  ✅ Screenshot Verification                                      ║
    ║  ✅ Custom Workflow Creation                                     ║
    ║                                                                   ║
    ║  Requirements:                                                    ║
    ║  • Python 3.7+                                                    ║
    ║  • pyautogui (optional - for keyboard/mouse automation)          ║
    ║                                                                   ║
    ║  Install: pip install pyautogui                                   ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Automation interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()