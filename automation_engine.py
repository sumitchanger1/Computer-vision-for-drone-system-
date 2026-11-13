import pyautogui
import time
import json
from pathlib import Path
from datetime import datetime
import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

class AutomationEngine:
    """
    Core automation engine for controlling mouse, keyboard, and windows
    """
    
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard_ctrl = KeyboardController()
        
        # Safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.1  # Small delay between actions
        
        # Recording state
        self.is_recording = False
        self.recorded_actions = []
        
        print("🤖 Automation Engine Initialized")
        print("⚠️  FAILSAFE: Move mouse to top-left corner to stop")
    
    # ============================================
    # MOUSE CONTROL
    # ============================================
    
    def click(self, x=None, y=None, button='left', clicks=1, interval=0.1):
        """Click at position or current position"""
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
            print(f"🖱️  Clicked at ({x}, {y}) - {button} button")
        else:
            pyautogui.click(clicks=clicks, interval=interval, button=button)
            print(f"🖱️  Clicked at current position - {button} button")
        
        return {"action": "click", "x": x, "y": y, "button": button, "clicks": clicks}
    
    def double_click(self, x=None, y=None):
        """Double click at position"""
        return self.click(x, y, clicks=2)
    
    def right_click(self, x=None, y=None):
        """Right click at position"""
        return self.click(x, y, button='right')
    
    def move_mouse(self, x, y, duration=0.5):
        """Move mouse smoothly to position"""
        pyautogui.moveTo(x, y, duration=duration)
        print(f"🖱️  Moved mouse to ({x}, {y})")
        return {"action": "move", "x": x, "y": y, "duration": duration}
    
    def drag(self, x, y, duration=0.5):
        """Drag mouse to position"""
        pyautogui.drag(x, y, duration=duration)
        print(f"🖱️  Dragged to ({x}, {y})")
        return {"action": "drag", "x": x, "y": y}
    
    def get_mouse_position(self):
        """Get current mouse position"""
        x, y = pyautogui.position()
        return {"x": x, "y": y}
    
    # ============================================
    # KEYBOARD CONTROL
    # ============================================
    
    def type_text(self, text, interval=0.05):
        """Type text with optional delay between characters"""
        pyautogui.write(text, interval=interval)
        print(f"⌨️  Typed: {text}")
        return {"action": "type", "text": text}
    
    def press_key(self, key):
        """Press a single key"""
        pyautogui.press(key)
        print(f"⌨️  Pressed: {key}")
        return {"action": "press", "key": key}
    
    def hotkey(self, *keys):
        """Press multiple keys together (e.g., Ctrl+C)"""
        pyautogui.hotkey(*keys)
        keys_str = "+".join(keys)
        print(f"⌨️  Hotkey: {keys_str}")
        return {"action": "hotkey", "keys": list(keys)}
    
    def hold_key(self, key, duration=1):
        """Hold a key for specified duration"""
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        print(f"⌨️  Held {key} for {duration}s")
        return {"action": "hold", "key": key, "duration": duration}
    
    # ============================================
    # SCREEN OPERATIONS
    # ============================================
    
    def screenshot(self, region=None, filename=None):
        """Take a screenshot"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = Path("data/screenshots") / filename
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        if region:
            img = pyautogui.screenshot(region=region)
        else:
            img = pyautogui.screenshot()
        
        img.save(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
        return {"action": "screenshot", "path": str(screenshot_path)}
    
    def find_image(self, image_path, confidence=0.8):
        """Find image on screen and return its position"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"🔍 Found image at {center}")
                return {"found": True, "x": center.x, "y": center.y}
            else:
                print(f"❌ Image not found: {image_path}")
                return {"found": False}
        except Exception as e:
            print(f"❌ Error finding image: {e}")
            return {"found": False, "error": str(e)}
    
    def wait_for_image(self, image_path, timeout=10, interval=0.5):
        """Wait for image to appear on screen"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.find_image(image_path)
            if result.get("found"):
                return result
            time.sleep(interval)
        
        print(f"⏱️  Timeout waiting for image: {image_path}")
        return {"found": False, "timeout": True}
    
    # ============================================
    # WINDOW OPERATIONS
    # ============================================
    
    def get_active_window(self):
        """Get information about active window"""
        try:
            import pygetwindow as gw
            active = gw.getActiveWindow()
            if active:
                return {
                    "title": active.title,
                    "x": active.left,
                    "y": active.top,
                    "width": active.width,
                    "height": active.height
                }
        except Exception as e:
            print(f"⚠️  Could not get active window: {e}")
            return None
    
    # ============================================
    # ACTION EXECUTION
    # ============================================
    
    def execute_action(self, action):
        """Execute a single action from JSON"""
        action_type = action.get("action")
        
        if action_type == "click":
            self.click(action.get("x"), action.get("y"), 
                      action.get("button", "left"), 
                      action.get("clicks", 1))
        
        elif action_type == "type":
            self.type_text(action.get("text", ""))
        
        elif action_type == "press":
            self.press_key(action.get("key"))
        
        elif action_type == "hotkey":
            self.hotkey(*action.get("keys", []))
        
        elif action_type == "move":
            self.move_mouse(action.get("x"), action.get("y"), 
                           action.get("duration", 0.5))
        
        elif action_type == "wait":
            duration = action.get("duration", 1)
            print(f"⏱️  Waiting {duration}s...")
            time.sleep(duration)
        
        else:
            print(f"⚠️  Unknown action type: {action_type}")
    
    def execute_workflow(self, workflow_file):
        """Execute a workflow from JSON file"""
        workflow_path = Path(workflow_file)
        
        if not workflow_path.exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            return False
        
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        print("\n" + "="*60)
        print(f"🚀 EXECUTING WORKFLOW: {workflow.get('name', 'Unnamed')}")
        print("="*60)
        
        actions = workflow.get("actions", [])
        
        if not actions:
            print("⚠️  No actions in workflow")
            return False
        
        print(f"📋 Total actions: {len(actions)}")
        print("\n⏱️  Starting in 3 seconds... (Move mouse to corner to abort)")
        time.sleep(3)
        
        for i, action in enumerate(actions, 1):
            print(f"\n[{i}/{len(actions)}] ", end="")
            
            try:
                self.execute_action(action)
            except pyautogui.FailSafeException:
                print("\n⚠️  FAILSAFE TRIGGERED - Automation stopped!")
                return False
            except Exception as e:
                print(f"\n❌ Error executing action: {e}")
                return False
            
            # Small delay between actions
            time.sleep(0.2)
        
        print("\n" + "="*60)
        print("✅ WORKFLOW COMPLETED!")
        print("="*60)
        
        return True
    
    # ============================================
    # WORKFLOW CREATION
    # ============================================
    
    def create_workflow(self, name, actions, description=""):
        """Create and save a workflow"""
        workflow = {
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "actions": actions
        }
        
        workflow_dir = Path("data/workflows")
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_file = workflow_dir / f"{name.lower().replace(' ', '_')}.json"
        
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"💾 Workflow saved: {workflow_file}")
        return workflow_file

# ============================================
# UTILITY FUNCTIONS
# ============================================

def demo_workflow():
    """Demo workflow showing capabilities"""
    engine = AutomationEngine()
    
    print("\n🎯 DEMO: Simple Automation")
    print("This will:")
    print("1. Get mouse position")
    print("2. Take a screenshot")
    print("3. Open Notepad")
    print("4. Type some text")
    print("\nPress Enter to start...")
    input()
    
    # Get current mouse position
    pos = engine.get_mouse_position()
    print(f"Current mouse: {pos}")
    
    # Take screenshot
    engine.screenshot()
    
    # Open Notepad
    print("\n📝 Opening Notepad...")
    engine.hotkey('win', 'r')
    time.sleep(1)
    engine.type_text('notepad')
    engine.press_key('enter')
    time.sleep(2)
    
    # Type text
    engine.type_text('Hello from Automation Engine!\n')
    engine.type_text('This is automated typing.\n')
    
    print("\n✅ Demo complete!")

if __name__ == "__main__":
    demo_workflow()