import json
import requests
from pathlib import Path
from datetime import datetime

class AIPatternRecognition:
    """
    Phase 3: AI-Powered Pattern Recognition with Ollama
    Uses local LLM to understand user behavior and suggest automations
    """
    
    def __init__(self, model="llama3.2:3b", ollama_url="http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
        
        self.data_dir = Path("data")
        self.patterns_dir = self.data_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflow_db = self.patterns_dir / "ai_workflows.json"
        self.load_workflow_history()
        
        # Test connection
        self.test_ollama_connection()
    
    def test_ollama_connection(self):
        """Test if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Connected to Ollama successfully!")
                models = response.json().get('models', [])
                print(f"📦 Available models: {[m['name'] for m in models]}")
            else:
                print("⚠️  Ollama is running but response unexpected")
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to Ollama!")
            print(f"   Make sure Ollama is running: ollama serve")
            print(f"   Error: {e}")
    
    def load_workflow_history(self):
        """Load workflow history"""
        if self.workflow_db.exists():
            with open(self.workflow_db, 'r') as f:
                self.workflow_history = json.load(f)
        else:
            self.workflow_history = {
                "sessions": [],
                "patterns": {},
                "total_analyzed": 0
            }
    
    def save_workflow_history(self):
        """Save workflow history"""
        with open(self.workflow_db, 'w') as f:
            json.dump(self.workflow_history, f, indent=2)
    
    def query_llm(self, prompt, temperature=0.7):
        """Query Ollama LLM"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"❌ LLM query failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error querying LLM: {e}")
            return None
    
    def analyze_session(self, events_json_path):
        """
        Main analysis: Use AI to understand user behavior
        """
        print("\n" + "="*60)
        print("🧠 AI-POWERED PATTERN RECOGNITION (Phase 3)")
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
        
        # Extract data
        transcript = self.extract_transcript(events)
        screen_events = [e for e in events if e.get("type") == "screen_change"]
        
        print(f"🎤 Transcript: {transcript[:100]}...")
        print(f"🖥️  Screen changes: {len(screen_events)}")
        
        # Create AI analysis prompt
        print("\n🤖 Querying AI for pattern analysis...")
        
        analysis_result = self.ai_analyze_workflow(transcript, screen_events)
        
        if not analysis_result:
            print("❌ AI analysis failed, using fallback")
            return self.fallback_analysis(session_id, transcript, screen_events)
        
        # Parse AI response
        insights = {
            "session_id": session_id,
            "analyzed_at": datetime.now().isoformat(),
            "transcript": transcript,
            "screen_changes": len(screen_events),
            "ai_analysis": analysis_result,
            "workflow_description": "",
            "detected_patterns": [],
            "automation_suggestions": []
        }
        
        # Extract structured data from AI response
        insights = self.parse_ai_response(insights, analysis_result)
        
        # Save insights
        self.save_insights(session_id, insights)
        
        # Display results
        self.display_insights(insights)
        
        # Update history
        self.update_workflow_history(insights)
        
        return insights
    
    def ai_analyze_workflow(self, transcript, screen_events):
        """Use AI to analyze the workflow"""
        
        # Build context
        context = f"""You are analyzing a desktop automation recording session to understand user behavior and suggest automation opportunities.

TRANSCRIPT (what user said):
"{transcript}"

SCREEN ACTIVITY:
- Total screen changes: {len(screen_events)}
- Change types: {self.summarize_changes(screen_events)}

Your task is to:
1. Understand what the user was doing
2. Identify any repetitive patterns
3. Suggest if this workflow can be automated
4. Provide specific automation steps

Format your response as:

WORKFLOW DESCRIPTION:
[Describe what the user was doing in 2-3 sentences]

DETECTED PATTERNS:
[List any repetitive actions or patterns you notice]

AUTOMATION POTENTIAL:
[Rate from 1-10 how automatable this is]

SUGGESTED AUTOMATION:
[If automatable, describe the specific automation steps]

Be specific and actionable. Focus on practical automation possibilities."""

        print("   Sending context to AI...")
        response = self.query_llm(context, temperature=0.7)
        
        if response:
            print("   ✅ AI analysis complete!")
        else:
            print("   ❌ AI analysis failed")
        
        return response
    
    def summarize_changes(self, screen_events):
        """Summarize screen change types"""
        change_types = {}
        for event in screen_events:
            change_type = event.get('change_type', 'unknown')
            change_types[change_type] = change_types.get(change_type, 0) + 1
        return ', '.join([f"{k}: {v}" for k, v in change_types.items()])
    
    def parse_ai_response(self, insights, ai_response):
        """Parse AI response into structured format"""
        
        # Extract sections from AI response
        sections = {
            'workflow_description': '',
            'detected_patterns': [],
            'automation_potential': 0,
            'suggested_automation': ''
        }
        
        current_section = None
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if 'WORKFLOW DESCRIPTION:' in line.upper():
                current_section = 'workflow_description'
                continue
            elif 'DETECTED PATTERNS:' in line.upper():
                current_section = 'detected_patterns'
                continue
            elif 'AUTOMATION POTENTIAL:' in line.upper():
                current_section = 'automation_potential'
                continue
            elif 'SUGGESTED AUTOMATION:' in line.upper():
                current_section = 'suggested_automation'
                continue
            
            if current_section and line:
                if current_section == 'detected_patterns':
                    if line.startswith('-') or line.startswith('•'):
                        sections['detected_patterns'].append(line.lstrip('-• '))
                elif current_section == 'automation_potential':
                    # Extract number
                    import re
                    match = re.search(r'(\d+)', line)
                    if match:
                        sections['automation_potential'] = int(match.group(1))
                else:
                    sections[current_section] += line + ' '
        
        # Update insights
        insights['workflow_description'] = sections['workflow_description'].strip()
        insights['detected_patterns'] = sections['detected_patterns']
        insights['automation_potential'] = sections['automation_potential']
        
        # Create automation suggestion
        if sections['suggested_automation'].strip():
            insights['automation_suggestions'] = [{
                "title": "AI-Detected Automation Opportunity",
                "description": sections['suggested_automation'].strip(),
                "confidence": sections['automation_potential'] / 10.0,
                "detected_by": "AI (Ollama LLM)"
            }]
        
        return insights
    
    def fallback_analysis(self, session_id, transcript, screen_events):
        """Fallback analysis if AI fails"""
        return {
            "session_id": session_id,
            "analyzed_at": datetime.now().isoformat(),
            "transcript": transcript,
            "screen_changes": len(screen_events),
            "workflow_description": f"User activity with {len(screen_events)} screen changes. Transcript: {transcript[:100]}...",
            "detected_patterns": ["Screen activity detected"],
            "automation_suggestions": [],
            "ai_analysis": "AI analysis unavailable"
        }
    
    def extract_transcript(self, events):
        """Extract transcript from events"""
        for event in events:
            if event.get("type") == "audio_transcript":
                return event.get("text", "")
        return ""
    
    def save_insights(self, session_id, insights):
        """Save insights to JSON"""
        insights_file = self.patterns_dir / f"{session_id}_ai_insights.json"
        
        with open(insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
        
        print(f"\n💾 AI insights saved: {insights_file}")
    
    def display_insights(self, insights):
        """Display AI analysis results"""
        print("\n" + "="*60)
        print("🤖 AI ANALYSIS RESULTS")
        print("="*60)
        
        print(f"\n🎤 TRANSCRIPT:")
        print(f"   {insights['transcript']}")
        
        print(f"\n📝 WORKFLOW DESCRIPTION:")
        print(f"   {insights['workflow_description']}")
        
        if insights.get('detected_patterns'):
            print(f"\n🔍 DETECTED PATTERNS:")
            for pattern in insights['detected_patterns']:
                print(f"   • {pattern}")
        
        if insights.get('automation_potential'):
            print(f"\n📊 AUTOMATION POTENTIAL: {insights['automation_potential']}/10")
        
        print(f"\n🚀 AUTOMATION SUGGESTIONS:")
        print("="*60)
        
        if insights['automation_suggestions']:
            for i, suggestion in enumerate(insights['automation_suggestions'], 1):
                print(f"\n{i}. {suggestion['title']}")
                print(f"   {suggestion['description']}")
                print(f"   Confidence: {suggestion['confidence']*100:.0f}%")
                print(f"   Detected by: {suggestion.get('detected_by', 'System')}")
        else:
            print("   No specific automations detected.")
            print("   Record more complex workflows to get suggestions.")
        
        print("\n" + "="*60)
        print("✅ AI Analysis Complete!")
        print("="*60)
    
    def update_workflow_history(self, insights):
        """Update workflow history"""
        self.workflow_history['sessions'].append({
            "session_id": insights['session_id'],
            "analyzed_at": insights['analyzed_at'],
            "automation_potential": insights.get('automation_potential', 0),
            "suggestions": len(insights['automation_suggestions'])
        })
        
        self.workflow_history['total_analyzed'] += 1
        self.save_workflow_history()

def main():
    """Main menu for AI pattern recognition"""
    
    print("🚀 Initializing AI Pattern Recognition Engine...")
    engine = AIPatternRecognition()
    
    while True:
        print("\n" + "="*60)
        print("🧠 AI PATTERN RECOGNITION - PHASE 3")
        print("="*60)
        print("\n1. Analyze latest recording with AI")
        print("2. Analyze specific recording")
        print("3. Show workflow history")
        print("4. Test AI connection")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            json_dir = Path("data/processed/json")
            if json_dir.exists():
                json_files = sorted(
                    json_dir.glob("*_events.json"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )
                if json_files:
                    print(f"\n🎯 Analyzing: {json_files[0].name}")
                    engine.analyze_session(json_files[0])
                else:
                    print("❌ No recordings found")
            else:
                print("❌ No processed data found")
        
        elif choice == '2':
            json_dir = Path("data/processed/json")
            if json_dir.exists():
                json_files = list(json_dir.glob("*_events.json"))
                if json_files:
                    print("\n📂 Available recordings:")
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
                print("❌ No data found")
        
        elif choice == '3':
            print("\n" + "="*60)
            print("📚 AI WORKFLOW HISTORY")
            print("="*60)
            
            history = engine.workflow_history
            print(f"\nTotal sessions analyzed: {history['total_analyzed']}")
            
            if history['sessions']:
                print("\nRecent sessions:")
                for session in history['sessions'][-5:]:
                    print(f"   • {session['session_id']}")
                    print(f"     Automation potential: {session.get('automation_potential', 'N/A')}/10")
                    print(f"     Suggestions: {session['suggestions']}")
        
        elif choice == '4':
            engine.test_ollama_connection()
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()