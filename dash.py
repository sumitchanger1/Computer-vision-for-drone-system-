import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import json
from datetime import datetime
import os
import wave
import pyaudio
import whisper
from PIL import Image
import mss
import easyocr
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize components
class DashcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Dashcam - Screen & Audio Insight Generator")
        self.root.geometry("800x600")
        
        # UI Elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg="green", fg="white")
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", state="disabled")
        self.stop_button.pack(pady=5)
        
        self.insights_text = scrolledtext.ScrolledText(root, width=90, height=30)
        self.insights_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # App state
        self.recording = False
        self.audio_thread = None
        self.screen_thread = None
        
        # Initialize models (load once)
        self.log("Initializing models...")
        self.whisper_model = whisper.load_model("base")  # Local Whisper for transcription
        self.ocr_reader = easyocr.Reader(['en'])  # OCR for screen text
        self.llm_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.llm_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.llm_generator = pipeline("text-generation", model=self.llm_model, tokenizer=self.llm_tokenizer, device=0 if torch.cuda.is_available() else -1)
        self.log("Models initialized.")
        
        # Audio setup
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.audio = pyaudio.PyAudio()
        self.audio_frames = []
        
        # Screen capture setup
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # Primary monitor
        
        # Output directory
        self.output_dir = "dashcam_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.insights_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.insights_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_recording(self):
        self.recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.audio_frames = []
        
        # Start threads
        self.audio_thread = threading.Thread(target=self.capture_audio, daemon=True)
        self.audio_thread.start()
        self.screen_thread = threading.Thread(target=self.capture_screen, daemon=True)
        self.screen_thread.start()
        
        self.log("Recording started: Capturing screen and audio...")
    
    def stop_recording(self):
        self.recording = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Recording stopped. Processing insights...")
        
        # Process final audio
        self.save_and_transcribe_audio()
        
        # Generate final insights
        self.generate_insights()
    
    def capture_audio(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while self.recording:
            data = stream.read(self.chunk)
            self.audio_frames.append(data)
        stream.stop_stream()
        stream.close()
    
    def save_and_transcribe_audio(self):
        if not self.audio_frames:
            return
        
        filename = os.path.join(self.output_dir, f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()
        
        self.log(f"Audio saved: {filename}")
        
        # Transcribe
        result = self.whisper_model.transcribe(filename)
        transcription = result["text"]
        self.log(f"Transcription: {transcription}")
        
        # Save transcription
        with open(filename.replace('.wav', '_transcription.txt'), 'w') as f:
            f.write(transcription)
    
    def capture_screen(self):
        screenshot_count = 0
        while self.recording:
            screenshot = self.sct.grab(self.monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            filename = os.path.join(self.output_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            img.save(filename)
            
            # OCR
            ocr_result = self.ocr_reader.readtext(img)
            screen_text = ' '.join([text[1] for text in ocr_result])
            
            # For now, log; later use in insights
            if screenshot_count % 10 == 0:  # Log every 10th to avoid spam
                self.log(f"Screen text sample: {screen_text[:100]}...")
            
            screenshot_count += 1
            time.sleep(1)  # Capture every second
    
    def generate_insights(self):
        # Mock collection of data; in real, aggregate from captures
        # For demo, assume some data
        screen_events = ["Mouse click at (x,y)", "Typing in text field", "Opening Excel"]  # Would come from captures
        transcription = "User is entering data into spreadsheet and saving."  # From audio
        
        # Structured JSON
        insights = {
            "timestamp": datetime.now().isoformat(),
            "screen_events": screen_events,
            "audio_transcription": transcription,
            "ui_actions": ["click", "type", "save"]
        }
        
        json_str = json.dumps(insights, indent=2)
        json_file = os.path.join(self.output_dir, f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_file, 'w') as f:
            f.write(json_str)
        
        self.log(f"Structured JSON saved: {json_file}")
        
        # Use LLM for description and suggestions
        prompt = f"Describe what's happening based on these events: {screen_events}. Audio: {transcription}. Suggest automations."
        
        response = self.llm_generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']
        
        self.log(f"LLM Insights: {response}")
        
        # Example suggestion
        suggestion = "Detected repetitive action: Opening Excel → Typing values → Saving file. Can be automated with a script."
        self.log(f"Automation Suggestion: {suggestion}")

def main():
    root = tk.Tk()
    app = DashcamApp(root)
    root.mainloop()
    
    # Cleanup
    app.audio.terminate()

if __name__ == "__main__":
    main()