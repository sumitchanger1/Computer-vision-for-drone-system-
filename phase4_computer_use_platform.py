"""
PHASE 4: COMPUTER USE PLATFORM
Task Automation System - Automates day-to-day user activities

Capabilities:
✅ Click buttons
✅ Type into forms  
✅ Navigate between windows
✅ Perform browser and file operations
"""

import pyautogui
import time
import json
from pathlib import Path
from datetime import datetime

class ComputerUsePlatform:
    """
    Computer Use Platform for automating desktop tasks
    """
    
    def __init__(self):
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        print("\n" + "="*70)
        print("🤖 COMPUTER USE PLATFORM - PHASE 4")
        print("="*70)
        print("   Automates day-to-day user activities")
        print("   ⚠️  SAFETY: Move mouse to corner to abort")
        print("="*70)
    
    # ============================================
    # CORE AUTOMATION CAPABILITIES
    # ============================================
    
    def click_button(self, x, y, button='left'):
        """✅ Capability 1: Click buttons"""
        print(f"🖱️  Clicking button at ({x}, {y})...")
        pyautogui.click(x, y, button=button)
        time.sleep(0.3)
    
    def type_into_form(self, text):
        """✅ Capability 2: Type into forms"""
        print(f"⌨️  Typing: {text[:50]}...")
        pyautogui.write(text, interval=0.05)
        time.sleep(0.2)
    
    def navigate_windows(self, action='next'):
        """✅ Capability 3: Navigate between windows"""
        print(f"🪟 Navigating windows ({action})...")
        if action == 'next':
            pyautogui.hotkey('alt', 'tab')
        elif action == 'minimize':
            pyautogui.hotkey('win', 'd')
        elif action == 'maximize':
            pyautogui.hotkey('win', 'up')
        time.sleep(0.5)
    
    def file_operation(self, operation, filename=None):
        """✅ Capability 4: Perform file operations"""
        print(f"📁 File operation: {operation}...")
        
        if operation == 'open':
            pyautogui.hotkey('ctrl', 'o')
        elif operation == 'save':
            pyautogui.hotkey('ctrl', 's')
        elif operation == 'save_as':
            pyautogui.hotkey('ctrl', 'shift', 's')
        elif operation == 'new':
            pyautogui.hotkey('ctrl', 'n')
        
        time.sleep(0.5)
        
        if filename and operation in ['save', 'save_as']:
            pyautogui.write(filename)
            time.sleep(0.2)
            pyautogui.press('enter')
    
    def browser_operation(self, operation, url=None):
        """✅ Capability 4: Perform browser operations"""
        print(f"🌐 Browser operation: {operation}...")
        
        if operation == 'new_tab':
            pyautogui.hotkey('ctrl', 't')
        elif operation == 'close_tab':
            pyautogui.hotkey('ctrl', 'w')
        elif operation == 'refresh':
            pyautogui.hotkey('ctrl', 'r')
        elif operation == 'address_bar':
            pyautogui.hotkey('ctrl', 'l')
            if url:
                time.sleep(0.3)
                pyautogui.write(url)
                pyautogui.press('enter')
        
        time.sleep(0.5)
    
    # ============================================
    # PRE-BUILT DEMO WORKFLOWS
    # ============================================
    
    def demo_notepad_workflow(self):
        """
        Demo 1: Text File Creation
        Shows: File operations + Typing + Saving
        """
        print("\n" + "="*70)
        print("📝 DEMO 1: TEXT FILE CREATION WORKFLOW")
        print("="*70)
        print("\nThis will:")
        print("  1. Open Notepad")
        print("  2. Type content")
        print("  3. Save file")
        print("\n⏱️  Starting in 3 seconds...")
        time.sleep(3)
        
        # Step 1: Open Notepad
        print("\n[1/6] Opening Notepad...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        # Step 2: Type content
        print("[2/6] Typing content...")
        content = """Desktop AI Assistant - Automated File Creation

This file was created automatically by the Computer Use Platform!

Capabilities Demonstrated:
✅ File Operations
✅ Typing into forms
✅ Window navigation
✅ Automated workflow execution

Timestamp: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        pyautogui.write(content, interval=0.02)
        time.sleep(1)
        
        # Step 3: Save file
        print("[3/6] Saving file...")
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        
        print("[4/6] Entering filename...")
        pyautogui.write('automated_demo_file.txt')
        time.sleep(0.5)
        
        print("[5/6] Confirming save...")
        pyautogui.press('enter')
        time.sleep(1)
        
        print("[6/6] Closing Notepad...")
        pyautogui.hotkey('alt', 'f4')
        
        print("\n✅ Demo 1 Complete!")
        print("   File saved: automated_demo_file.txt")
    
    def demo_browser_workflow(self):
        """
        Demo 2: Browser Automation
        Shows: Browser operations + Navigation + Typing
        """
        print("\n" + "="*70)
        print("🌐 DEMO 2: BROWSER AUTOMATION WORKFLOW")
        print("="*70)
        print("\nThis will:")
        print("  1. Open browser")
        print("  2. Navigate to URL")
        print("  3. Demonstrate browser controls")
        print("\n⏱️  Starting in 3 seconds...")
        time.sleep(3)
        
        # Step 1: Open browser
        print("\n[1/5] Opening browser...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        # Try common browsers
        pyautogui.write('chrome')
        pyautogui.press('enter')
        time.sleep(3)
        
        # Step 2: Open new tab
        print("[2/5] Opening new tab...")
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        
        # Step 3: Type URL
        print("[3/5] Navigating to URL...")
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.write('https://www.google.com')
        pyautogui.press('enter')
        time.sleep(2)
        
        # Step 4: Type in search
        print("[4/5] Typing search query...")
        time.sleep(2)
        pyautogui.write('Desktop AI Assistant automation')
        time.sleep(1)
        
        print("[5/5] Demo complete!")
        
        print("\n✅ Demo 2 Complete!")
        print("   Browser automation demonstrated!")
    
    def demo_window_navigation(self):
        """
        Demo 3: Window Management
        Shows: Window navigation + Multi-tasking
        """
        print("\n" + "="*70)
        print("🪟 DEMO 3: WINDOW NAVIGATION WORKFLOW")
        print("="*70)
        print("\nThis will:")
        print("  1. Open multiple applications")
        print("  2. Navigate between windows")
        print("  3. Demonstrate window management")
        print("\n⏱️  Starting in 3 seconds...")
        time.sleep(3)
        
        # Open first app
        print("\n[1/6] Opening Calculator...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('calc')
        pyautogui.press('enter')
        time.sleep(2)
        
        # Open second app
        print("[2/6] Opening Notepad...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        # Navigate between windows
        print("[3/6] Switching to Calculator...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        
        print("[4/6] Switching back to Notepad...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        
        # Minimize all
        print("[5/6] Minimizing all windows...")
        pyautogui.hotkey('win', 'd')
        time.sleep(1)
        
        print("[6/6] Showing windows again...")
        pyautogui.hotkey('win', 'd')
        
        print("\n✅ Demo 3 Complete!")
        print("   Window navigation demonstrated!")
    
    def demo_form_filling(self):
        """
        Demo 4: Form Filling Automation
        Shows: Complex typing + Tab navigation + Form submission
        """
        print("\n" + "="*70)
        print("📋 DEMO 4: FORM FILLING WORKFLOW")
        print("="*70)
        print("\nThis will:")
        print("  1. Open Notepad (as form simulation)")
        print("  2. Fill multiple fields")
        print("  3. Navigate with Tab key")
        print("  4. Demonstrate form automation")
        print("\n⏱️  Starting in 3 seconds...")
        time.sleep(3)
        
        # Open Notepad as form simulation
        print("\n[1/7] Opening application...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        # Simulate form filling
        print("[2/7] Filling Name field...")
        pyautogui.write('Name: John Doe')
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("[3/7] Filling Email field...")
        pyautogui.write('Email: john.doe@example.com')
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("[4/7] Filling Phone field...")
        pyautogui.write('Phone: +1-555-0123')
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("[5/7] Filling Address field...")
        pyautogui.write('Address: 123 Automation Street, Tech City')
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("[6/7] Adding submission note...")
        pyautogui.press('enter')
        pyautogui.write('Form filled automatically by Computer Use Platform!')
        time.sleep(1)
        
        print("[7/7] Closing without saving...")
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.5)
        pyautogui.press('right')  # Don't Save
        pyautogui.press('enter')
        
        print("\n✅ Demo 4 Complete!")
        print("   Form filling demonstrated!")
    
    # ============================================
    # MAIN MENU
    # ============================================
    
    def show_capabilities_menu(self):
        """Show available automation capabilities"""
        
        while True:
            print("\n" + "="*70)
            print("🤖 COMPUTER USE PLATFORM - AUTOMATION MENU")
            print("="*70)
            
            print("\n📋 CORE CAPABILITIES:")
            print("   1. ✅ Click Buttons Demo")
            print("   2. ✅ Type Into Forms Demo")
            print("   3. ✅ Navigate Windows Demo")
            print("   4. ✅ File Operations Demo")
            print("   5. ✅ Browser Operations Demo")
            
            print("\n🎬 COMPLETE WORKFLOWS:")
            print("   6. Demo 1: Text File Creation")
            print("   7. Demo 2: Browser Automation")
            print("   8. Demo 3: Window Navigation")
            print("   9. Demo 4: Form Filling")
            
            print("\n🚀 ALL DEMOS:")
            print("   10. Run ALL demos (complete showcase)")
            
            print("\n❌ EXIT:")
            print("   11. Exit")
            
            print("="*70)
            
            choice = input("\n👉 Select option (1-11): ").strip()
            
            try:
                if choice == '1':
                    self.demo_click_capability()
                elif choice == '2':
                    self.demo_typing_capability()
                elif choice == '3':
                    self.demo_navigation_capability()
                elif choice == '4':
                    self.demo_file_capability()
                elif choice == '5':
                    self.demo_browser_capability()
                elif choice == '6':
                    self.demo_notepad_workflow()
                elif choice == '7':
                    self.demo_browser_workflow()
                elif choice == '8':
                    self.demo_window_navigation()
                elif choice == '9':
                    self.demo_form_filling()
                elif choice == '10':
                    self.run_all_demos()
                elif choice == '11':
                    print("\n👋 Thank you for using Computer Use Platform!")
                    break
                else:
                    print("\n❌ Invalid option!")
                    
                input("\n⏸️  Press Enter to continue...")
                
            except pyautogui.FailSafeException:
                print("\n⚠️  FAILSAFE ACTIVATED - Automation stopped!")
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
    
    def demo_click_capability(self):
        """Demo: Click buttons capability"""
        print("\n" + "="*70)
        print("🖱️  CAPABILITY 1: CLICK BUTTONS")
        print("="*70)
        print("\nMove your mouse over the Start button")
        print("The system will click it in 5 seconds...")
        time.sleep(5)
        
        # Click Windows Start button (bottom-left)
        pyautogui.click(10, pyautogui.size()[1] - 10)
        time.sleep(1)
        pyautogui.press('esc')
        
        print("\n✅ Click capability demonstrated!")
    
    def demo_typing_capability(self):
        """Demo: Type into forms capability"""
        print("\n" + "="*70)
        print("⌨️  CAPABILITY 2: TYPE INTO FORMS")
        print("="*70)
        print("\nOpening Notepad to demonstrate typing...")
        time.sleep(2)
        
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        print("Typing demonstration text...")
        pyautogui.write('This demonstrates automated typing into forms and applications!')
        time.sleep(1)
        
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.5)
        pyautogui.press('right')
        pyautogui.press('enter')
        
        print("\n✅ Typing capability demonstrated!")
    
    def demo_navigation_capability(self):
        """Demo: Navigate windows capability"""
        print("\n" + "="*70)
        print("🪟 CAPABILITY 3: NAVIGATE WINDOWS")
        print("="*70)
        print("\nOpening multiple windows and navigating...")
        time.sleep(2)
        
        # Open two apps
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('calc')
        pyautogui.press('enter')
        time.sleep(2)
        
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        print("Navigating between windows...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        
        # Close apps
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'f4')
        
        print("\n✅ Window navigation demonstrated!")
    
    def demo_file_capability(self):
        """Demo: File operations capability"""
        print("\n" + "="*70)
        print("📁 CAPABILITY 4: FILE OPERATIONS")
        print("="*70)
        print("\nDemonstrating file operations...")
        time.sleep(2)
        
        # Open, type, save
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('notepad')
        pyautogui.press('enter')
        time.sleep(2)
        
        pyautogui.write('File operations demo!')
        time.sleep(1)
        
        print("Saving file...")
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        pyautogui.write('file_ops_demo.txt')
        pyautogui.press('enter')
        time.sleep(1)
        
        pyautogui.hotkey('alt', 'f4')
        
        print("\n✅ File operations demonstrated!")
    
    def demo_browser_capability(self):
        """Demo: Browser operations capability"""
        print("\n" + "="*70)
        print("🌐 CAPABILITY 4: BROWSER OPERATIONS")
        print("="*70)
        print("\nNote: This requires a browser to be installed")
        print("Demo will attempt to open Chrome/Edge")
        time.sleep(2)
        
        print("Opening browser...")
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write('chrome')
        pyautogui.press('enter')
        time.sleep(3)
        
        print("Opening new tab...")
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        
        print("\n✅ Browser operations demonstrated!")
    
    def run_all_demos(self):
        """Run all demos in sequence"""
        print("\n" + "="*70)
        print("🚀 RUNNING ALL DEMOS")
        print("="*70)
        print("\nThis will run all 4 workflow demos:")
        print("  1. Text File Creation")
        print("  2. Browser Automation")
        print("  3. Window Navigation")
        print("  4. Form Filling")
        print("\n⏱️  Total time: ~2-3 minutes")
        
        confirm = input("\nContinue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
        
        self.demo_notepad_workflow()
        input("\n⏸️  Press Enter for next demo...")
        
        self.demo_browser_workflow()
        input("\n⏸️  Press Enter for next demo...")
        
        self.demo_window_navigation()
        input("\n⏸️  Press Enter for next demo...")
        
        self.demo_form_filling()
        
        print("\n" + "="*70)
        print("🎉 ALL DEMOS COMPLETE!")
        print("="*70)
        print("\nCapabilities Demonstrated:")
        print("  ✅ Click buttons")
        print("  ✅ Type into forms")
        print("  ✅ Navigate between windows")
        print("  ✅ Perform file operations")
        print("  ✅ Perform browser operations")
        print("="*70)

def main():
    """Main entry point"""
    platform = ComputerUsePlatform()
    platform.show_capabilities_menu()

if __name__ == "__main__":
    main()