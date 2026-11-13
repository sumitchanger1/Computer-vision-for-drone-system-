from automation_engine import AutomationEngine
import json
from pathlib import Path

class WorkflowBuilder:
    """
    Build workflows from recorded events or manual actions
    """
    
    def __init__(self):
        self.engine = AutomationEngine()
    
    def convert_events_to_workflow(self, events_json_path):
        """Convert Phase 2 JSON events into executable workflow"""
        
        print("="*60)
        print("🔄 CONVERTING EVENTS TO WORKFLOW")
        print("="*60)
        
        events_path = Path(events_json_path)
        
        if not events_path.exists():
            print(f"❌ Events file not found: {events_json_path}")
            return None
        
        with open(events_path, 'r') as f:
            data = json.load(f)
        
        session_id = data.get("session_id", "unknown")
        events = data.get("events", [])
        
        print(f"📋 Session: {session_id}")
        print(f"📊 Total events: {len(events)}")
        
        # Extract actions from events
        actions = []
        transcript = ""
        
        for event in events:
            event_type = event.get("type")
            
            if event_type == "audio_transcript":
                transcript = event.get("text", "")
                print(f"\n🎤 Transcript: {transcript}")
            
            elif event_type == "screen_change":
                timestamp = event.get("timestamp")
                change_type = event.get("change_type", "unknown")
                
                print(f"   [{timestamp}s] {change_type} change detected")
                
                # Add a placeholder action (will be refined with Phase 3)
                actions.append({
                    "action": "wait",
                    "duration": 0.5,
                    "note": f"Screen change at {timestamp}s - {change_type}"
                })
        
        # Create workflow
        workflow_name = f"workflow_{session_id}"
        description = f"Auto-generated from: {session_id}\nTranscript: {transcript}"
        
        workflow_path = self.engine.create_workflow(
            name=workflow_name,
            actions=actions,
            description=description
        )
        
        print(f"\n✅ Workflow created: {workflow_path}")
        print(f"📝 Actions: {len(actions)}")
        
        return workflow_path
    
    def create_custom_workflow(self):
        """Interactive workflow creator"""
        
        print("\n" + "="*60)
        print("🎨 CUSTOM WORKFLOW BUILDER")
        print("="*60)
        
        name = input("\nWorkflow name: ")
        description = input("Description: ")
        
        actions = []
        
        print("\n📋 Add actions (type 'done' when finished):")
        print("\nAvailable actions:")
        print("1. click - Click at position")
        print("2. type - Type text")
        print("3. hotkey - Press key combination")
        print("4. wait - Wait for duration")
        print("5. screenshot - Take screenshot")
        
        while True:
            action_type = input("\nAction type (or 'done'): ").strip().lower()
            
            if action_type == 'done':
                break
            
            if action_type == 'click':
                x = int(input("  X coordinate: "))
                y = int(input("  Y coordinate: "))
                button = input("  Button (left/right) [left]: ") or "left"
                actions.append({
                    "action": "click",
                    "x": x,
                    "y": y,
                    "button": button
                })
            
            elif action_type == 'type':
                text = input("  Text to type: ")
                actions.append({
                    "action": "type",
                    "text": text
                })
            
            elif action_type == 'hotkey':
                keys = input("  Keys (comma-separated, e.g., ctrl,c): ").split(',')
                keys = [k.strip() for k in keys]
                actions.append({
                    "action": "hotkey",
                    "keys": keys
                })
            
            elif action_type == 'wait':
                duration = float(input("  Duration (seconds): "))
                actions.append({
                    "action": "wait",
                    "duration": duration
                })
            
            elif action_type == 'screenshot':
                actions.append({
                    "action": "screenshot"
                })
            
            else:
                print("  ❌ Unknown action type")
                continue
            
            print(f"  ✅ Added {action_type} action")
        
        if not actions:
            print("\n⚠️  No actions added")
            return None
        
        workflow_path = self.engine.create_workflow(name, actions, description)
        print(f"\n✅ Workflow saved: {workflow_path}")
        
        return workflow_path
    
    def list_workflows(self):
        """List all available workflows"""
        
        workflow_dir = Path("data/workflows")
        
        if not workflow_dir.exists():
            print("📁 No workflows directory found")
            return []
        
        workflows = list(workflow_dir.glob("*.json"))
        
        if not workflows:
            print("📋 No workflows found")
            return []
        
        print("\n📋 Available Workflows:")
        print("="*60)
        
        for i, wf in enumerate(workflows, 1):
            with open(wf, 'r') as f:
                data = json.load(f)
            
            name = data.get("name", "Unnamed")
            desc = data.get("description", "No description")
            action_count = len(data.get("actions", []))
            
            print(f"\n{i}. {name}")
            print(f"   File: {wf.name}")
            print(f"   Actions: {action_count}")
            print(f"   Description: {desc[:100]}")
        
        print("="*60)
        
        return workflows

def main():
    """Main menu for workflow management"""
    
    builder = WorkflowBuilder()
    
    while True:
        print("\n" + "="*60)
        print("🤖 WORKFLOW MANAGER")
        print("="*60)
        print("\n1. Convert Phase 2 events to workflow")
        print("2. Create custom workflow")
        print("3. List all workflows")
        print("4. Execute a workflow")
        print("5. Demo automation")
        print("6. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            # Find latest events file
            json_dir = Path("data/processed/json")
            if json_dir.exists():
                json_files = sorted(json_dir.glob("*_events.json"), 
                                  key=lambda x: x.stat().st_mtime, 
                                  reverse=True)
                if json_files:
                    print(f"\nUsing latest: {json_files[0].name}")
                    builder.convert_events_to_workflow(json_files[0])
                else:
                    print("❌ No events files found")
            else:
                print("❌ No processed data found")
        
        elif choice == '2':
            builder.create_custom_workflow()
        
        elif choice == '3':
            builder.list_workflows()
        
        elif choice == '4':
            workflows = builder.list_workflows()
            if workflows:
                try:
                    idx = int(input("\nSelect workflow number: ")) - 1
                    if 0 <= idx < len(workflows):
                        builder.engine.execute_workflow(workflows[idx])
                    else:
                        print("❌ Invalid selection")
                except ValueError:
                    print("❌ Invalid input")
        
        elif choice == '5':
            from automation_engine import demo_workflow
            demo_workflow()
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()