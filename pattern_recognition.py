import json
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

class PatternRecognitionEngine:
    """
    Phase 3: Pattern Recognition & Workflow Analysis
    Analyzes user behavior and suggests automations
    """
    
    def __init__(self):
        self.data_dir = Path("data")
        self.patterns_dir = self.data_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflow_db = self.patterns_dir / "detected_workflows.json"
        self.load_workflow_history()
    
    def load_workflow_history(self):
        """Load previously detected workflows"""
        if self.workflow_db.exists():
            with open(self.workflow_db, 'r') as f:
                self.workflow_history = json.load(f)
        else:
            self.workflow_history = {
                "workflows": [],
                "patterns": {},
                "suggestions": []
            }
    
    def save_workflow_history(self):
        """Save detected workflows"""
        with open(self.workflow_db, 'w') as f:
            json.dump(self.workflow_history, f, indent=2)
    
    def analyze_session(self, events_json_path):
        """
        Main analysis function: Analyze a recording session
        Returns structured insights about user behavior
        """
        print("\n" + "="*60)
        print("🧠 PHASE 3: PATTERN RECOGNITION & ANALYSIS")
        print("="*60)
        
        # Load events
        events_path = Path(events_json_path)
        if not events_path.exists():
            print(f"❌ Events file not found: {events_json_path}")
            return None
        
        with open(events_path, 'r') as f:
            data = json.load(f)
        
        session_id = data.get("session_id", "unknown")
        events = data.get("events", [])
        
        print(f"\n📋 Analyzing session: {session_id}")
        print(f"📊 Total events: {len(events)}")
        
        # Extract insights
        insights = {
            "session_id": session_id,
            "analyzed_at": datetime.now().isoformat(),
            "transcript": self.extract_transcript(events),
            "screen_activity": self.analyze_screen_activity(events),
            "detected_actions": self.detect_actions(events),
            "workflow_description": "",
            "automation_suggestions": [],
            "confidence": 0.0
        }
        
        # Generate workflow description
        insights["workflow_description"] = self.generate_workflow_description(insights)
        
        # Generate automation suggestions
        insights["automation_suggestions"] = self.generate_automation_suggestions(insights)
        
        # Calculate confidence
        insights["confidence"] = self.calculate_confidence(insights)
        
        # Save insights
        self.save_insights(session_id, insights)
        
        # Display results
        self.display_insights(insights)
        
        # Update workflow history
        self.update_workflow_history(insights)
        
        return insights
    
    def extract_transcript(self, events):
        """Extract audio transcript from events"""
        for event in events:
            if event.get("type") == "audio_transcript":
                return event.get("text", "")
        return ""
    
    def analyze_screen_activity(self, events):
        """Analyze screen change events"""
        screen_events = [e for e in events if e.get("type") == "screen_change"]
        
        if not screen_events:
            return {"total_changes": 0, "change_types": {}}
        
        change_types = Counter(e.get("change_type", "unknown") for e in screen_events)
        
        return {
            "total_changes": len(screen_events),
            "change_types": dict(change_types),
            "timestamps": [e.get("timestamp") for e in screen_events],
            "avg_time_between_changes": self.calculate_avg_interval(screen_events)
        }
    
    def calculate_avg_interval(self, events):
        """Calculate average time between events"""
        if len(events) < 2:
            return 0
        
        timestamps = [e.get("timestamp", 0) for e in events]
        intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        
        return round(sum(intervals) / len(intervals), 2) if intervals else 0
    
    def detect_actions(self, events):
        """
        Detect specific actions from transcript and screen changes
        Uses keyword matching and heuristics
        """
        transcript = self.extract_transcript(events)
        screen_activity = self.analyze_screen_activity(events)
        
        detected_actions = []
        
        # Keyword-based action detection
        action_keywords = {
            "open": ["open", "opened", "opening", "start", "launch"],
            "save": ["save", "saved", "saving"],
            "type": ["type", "typed", "typing", "enter", "write"],
            "click": ["click", "clicked", "clicking", "press"],
            "close": ["close", "closed", "closing"],
            "copy": ["copy", "copied"],
            "paste": ["paste", "pasted"],
            "edit": ["edit", "edited", "editing", "modify"],
            "file": ["file", "document", "excel", "word", "notepad"],
            "browse": ["browse", "browser", "chrome", "firefox", "search"]
        }
        
        transcript_lower = transcript.lower()
        
        for action, keywords in action_keywords.items():
            for keyword in keywords:
                if keyword in transcript_lower:
                    detected_actions.append({
                        "action": action,
                        "keyword": keyword,
                        "source": "transcript"
                    })
                    break
        
        # Screen activity-based detection
        if screen_activity["total_changes"] > 5:
            detected_actions.append({
                "action": "multiple_operations",
                "count": screen_activity["total_changes"],
                "source": "screen_activity"
            })
        
        # Deduplicate actions
        unique_actions = []
        seen = set()
        for action in detected_actions:
            action_key = action["action"]
            if action_key not in seen:
                unique_actions.append(action)
                seen.add(action_key)
        
        return unique_actions
    
    def generate_workflow_description(self, insights):
        """
        Generate human-readable workflow description
        This simulates what an LLM would generate
        """
        transcript = insights["transcript"]
        actions = insights["detected_actions"]
        screen_activity = insights["screen_activity"]
        
        # Build description based on detected patterns
        description_parts = []
        
        # Analyze transcript
        if transcript:
            description_parts.append(f"User said: \"{transcript}\"")
        
        # Analyze actions
        action_names = [a["action"] for a in actions]
        
        if "open" in action_names and "save" in action_names:
            description_parts.append("Workflow involves opening and saving files")
        
        if "type" in action_names or "edit" in action_names:
            description_parts.append("User performed data entry or editing")
        
        if "file" in action_names:
            if "excel" in transcript.lower():
                description_parts.append("Working with Excel spreadsheet")
            elif "word" in transcript.lower():
                description_parts.append("Working with Word document")
            elif "notepad" in transcript.lower():
                description_parts.append("Working with text file")
            else:
                description_parts.append("Working with file operations")
        
        if "browse" in action_names:
            description_parts.append("Web browsing activity detected")
        
        # Analyze screen changes
        if screen_activity["total_changes"] > 10:
            description_parts.append("High activity session with multiple screen changes")
        elif screen_activity["total_changes"] > 5:
            description_parts.append("Moderate activity with several operations")
        else:
            description_parts.append("Simple workflow with few operations")
        
        # Combine description
        if description_parts:
            description = "Detected workflow: " + ". ".join(description_parts) + "."
        else:
            description = "Simple recording session with basic user activity."
        
        return description
    
    def generate_automation_suggestions(self, insights):
        """
        Generate automation suggestions based on detected patterns
        This is the KEY requirement: suggesting automatable workflows
        """
        suggestions = []
        
        actions = insights["detected_actions"]
        action_names = [a["action"] for a in actions]
        transcript = insights["transcript"].lower()
        screen_activity = insights["screen_activity"]
        
        # Pattern 1: Open → Edit → Save
        if "open" in action_names and "save" in action_names:
            if "type" in action_names or "edit" in action_names:
                suggestions.append({
                    "pattern": "open_edit_save",
                    "title": "File Editing Workflow",
                    "description": "Detected repetitive action: Opening file → Editing content → Saving file. Can be automated.",
                    "confidence": 0.85,
                    "automation_steps": [
                        "1. Automatically open target file",
                        "2. Apply predefined edits or templates",
                        "3. Save and close file"
                    ]
                })
        
        # Pattern 2: Excel operations
        if "excel" in transcript:
            suggestions.append({
                "pattern": "excel_workflow",
                "title": "Excel Data Entry",
                "description": "Detected repetitive action: Opening Excel → Typing values → Saving file. Can be automated.",
                "confidence": 0.80,
                "automation_steps": [
                    "1. Open Excel workbook",
                    "2. Navigate to specific cells",
                    "3. Enter data from template or source",
                    "4. Apply formulas",
                    "5. Save workbook"
                ]
            })
        
        # Pattern 3: Web browsing
        if "browse" in action_names or any(word in transcript for word in ["chrome", "browser", "search", "website"]):
            suggestions.append({
                "pattern": "web_automation",
                "title": "Web Browsing Task",
                "description": "Detected repetitive action: Opening browser → Navigating to site → Filling forms. Can be automated.",
                "confidence": 0.75,
                "automation_steps": [
                    "1. Open browser",
                    "2. Navigate to specific URL",
                    "3. Fill form fields automatically",
                    "4. Submit or extract data"
                ]
            })
        
        # Pattern 4: Copy-paste operations
        if "copy" in action_names and "paste" in action_names:
            suggestions.append({
                "pattern": "copy_paste_workflow",
                "title": "Data Transfer Task",
                "description": "Detected repetitive action: Copying data → Pasting to another location. Can be automated.",
                "confidence": 0.70,
                "automation_steps": [
                    "1. Extract data from source",
                    "2. Transform data if needed",
                    "3. Paste to destination automatically"
                ]
            })
        
        # Pattern 5: High-frequency operations
        if screen_activity["total_changes"] > 8:
            suggestions.append({
                "pattern": "repetitive_task",
                "title": "High-Frequency Task",
                "description": f"Detected {screen_activity['total_changes']} screen changes in short time. Repetitive task detected. Can be automated.",
                "confidence": 0.65,
                "automation_steps": [
                    "1. Record exact sequence of actions",
                    "2. Create macro or script",
                    "3. Execute with single command"
                ]
            })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return suggestions
    
    def calculate_confidence(self, insights):
        """Calculate overall confidence in analysis"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on data quality
        if insights["transcript"]:
            confidence += 0.2
        
        if len(insights["detected_actions"]) > 2:
            confidence += 0.15
        
        if insights["screen_activity"]["total_changes"] > 3:
            confidence += 0.15
        
        return min(confidence, 1.0)
    
    def save_insights(self, session_id, insights):
        """Save analysis insights to JSON"""
        insights_file = self.patterns_dir / f"{session_id}_insights.json"
        
        with open(insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
        
        print(f"\n💾 Insights saved: {insights_file}")
    
    def display_insights(self, insights):
        """Display analysis results in readable format"""
        print("\n" + "="*60)
        print("📊 ANALYSIS RESULTS")
        print("="*60)
        
        print(f"\n🎤 Transcript:")
        print(f"   {insights['transcript']}")
        
        print(f"\n🖥️  Screen Activity:")
        activity = insights["screen_activity"]
        print(f"   Total changes: {activity['total_changes']}")
        for change_type, count in activity.get("change_types", {}).items():
            print(f"   {change_type}: {count}")
        
        print(f"\n🎯 Detected Actions:")
        for action in insights["detected_actions"]:
            print(f"   • {action['action']} (from {action['source']})")
        
        print(f"\n📝 Workflow Description:")
        print(f"   {insights['workflow_description']}")
        
        print(f"\n🤖 AUTOMATION SUGGESTIONS:")
        print("="*60)
        
        suggestions = insights["automation_suggestions"]
        if not suggestions:
            print("   No automation patterns detected yet.")
            print("   Record more sessions to detect patterns.")
        else:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"\n{i}. {suggestion['title']}")
                print(f"   {suggestion['description']}")
                print(f"   Confidence: {suggestion['confidence']*100:.0f}%")
                print(f"   Steps:")
                for step in suggestion["automation_steps"]:
                    print(f"      {step}")
        
        print("\n" + "="*60)
        print(f"📈 Overall Confidence: {insights['confidence']*100:.0f}%")
        print("="*60)
    
    def update_workflow_history(self, insights):
        """Update workflow history for pattern learning"""
        self.workflow_history["workflows"].append({
            "session_id": insights["session_id"],
            "analyzed_at": insights["analyzed_at"],
            "confidence": insights["confidence"],
            "suggestions": len(insights["automation_suggestions"])
        })
        
        # Update pattern counts
        for suggestion in insights["automation_suggestions"]:
            pattern = suggestion["pattern"]
            self.workflow_history["patterns"][pattern] = \
                self.workflow_history["patterns"].get(pattern, 0) + 1
        
        self.save_workflow_history()

def main():
    """Main interface for pattern recognition"""
    
    engine = PatternRecognitionEngine()
    
    while True:
        print("\n" + "="*60)
        print("🧠 PATTERN RECOGNITION ENGINE - PHASE 3")
        print("="*60)
        print("\n1. Analyze latest recording")
        print("2. Analyze specific recording")
        print("3. Show workflow history")
        print("4. Show all insights")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            # Find latest events file
            json_dir = Path("data/processed/json")
            if json_dir.exists():
                json_files = sorted(
                    json_dir.glob("*_events.json"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )
                if json_files:
                    print(f"\nAnalyzing: {json_files[0].name}")
                    engine.analyze_session(json_files[0])
                else:
                    print("❌ No processed recordings found")
            else:
                print("❌ No processed data directory found")
        
        elif choice == '2':
            json_dir = Path("data/processed/json")
            if json_dir.exists():
                json_files = list(json_dir.glob("*_events.json"))
                if json_files:
                    print("\nAvailable recordings:")
                    for i, f in enumerate(json_files, 1):
                        print(f"   {i}. {f.name}")
                    
                    try:
                        idx = int(input("\nSelect number: ")) - 1
                        if 0 <= idx < len(json_files):
                            engine.analyze_session(json_files[idx])
                        else:
                            print("❌ Invalid selection")
                    except ValueError:
                        print("❌ Invalid input")
                else:
                    print("❌ No recordings found")
            else:
                print("❌ No processed data found")
        
        elif choice == '3':
            print("\n" + "="*60)
            print("📚 WORKFLOW HISTORY")
            print("="*60)
            
            history = engine.workflow_history
            print(f"\nTotal analyzed sessions: {len(history['workflows'])}")
            print(f"\nDetected patterns:")
            for pattern, count in history['patterns'].items():
                print(f"   {pattern}: {count} times")
        
        elif choice == '4':
            patterns_dir = Path("data/patterns")
            if patterns_dir.exists():
                insight_files = list(patterns_dir.glob("*_insights.json"))
                print(f"\nFound {len(insight_files)} analysis results:")
                for f in insight_files:
                    print(f"   • {f.name}")
            else:
                print("❌ No insights found")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()