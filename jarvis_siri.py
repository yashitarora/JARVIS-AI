#!/usr/bin/env python3
"""
JARVIS Siri-Like Assistant
Say "Hey Jarvis" -> Glowing circle appears -> Listens -> Responds -> Disappears
"""

import os
import sys
import time
import json
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import font as tkfont
import math
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================
JARVIS_DIR = Path(__file__).parent
LOGO = "J.A.R.V.I.S"
WAKE_WORDS = ["hey jarvis", "hey jarvis", "hey jarvis", "jarvis"]
VOICE = "Samantha"  # macOS voice (Samantha, Alex, Daniel, Karen, etc.)
VOICE_RATE = 200    # Words per minute (150-250 is natural)
LISTEN_TIMEOUT = 8  # Seconds to wait for command after wake

# ============================================================
# COMMAND HANDLER - Responds to everything
# ============================================================
class Brain:
    """Process any voice command and respond."""

    def __init__(self):
        import datetime
        self.dt = datetime
        self.home = str(Path.home())

        # App map
        self.apps = {
            "chrome": "/Applications/Google Chrome.app",
            "google chrome": "/Applications/Google Chrome.app",
            "safari": "/Applications/Safari.app",
            "firefox": "/Applications/Firefox.app",
            "terminal": "/Applications/Utilities/Terminal.app",
            "vs code": "/Applications/Visual Studio Code.app",
            "vscode": "/Applications/Visual Studio Code.app",
            "visual studio code": "/Applications/Visual Studio Code.app",
            "whatsapp": "/Applications/WhatsApp.app",
            "spotify": "/Applications/Spotify.app",
            "netflix": "/Applications/Netflix.app",
            "notes": "/Applications/Notes.app",
            "finder": "/System/Library/CoreServices/Finder.app",
            "music": "/Applications/Music.app",
            "photos": "/Applications/Photos.app",
            "calendar": "/Applications/Calendar.app",
            "messages": "/Applications/Messages.app",
            "facetime": "/Applications/FaceTime.app",
            "settings": "/Applications/System Settings.app",
            "calculator": "/Applications/Calculator.app",
            "textedit": "/Applications/TextEdit.app",
            "preview": "/Applications/Preview.app",
            "reminders": "/Applications/Reminders.app",
            "maps": "/Applications/Maps.app",
            "mail": "/Applications/Mail.app",
            "pages": "/Applications/Pages.app",
            "numbers": "/Applications/Numbers.app",
            "keynote": "/Applications/Keynote.app",
            "xcode": "/Applications/Xcode.app",
            "slack": "/Applications/Slack.app",
            "discord": "/Applications/Discord.app",
            "zoom": "/Applications/zoom.us.app",
            "teams": "/Applications/Microsoft Teams.app",
            "word": "/Applications/Microsoft Word.app",
            "excel": "/Applications/Microsoft Excel.app",
            "powerpoint": "/Applications/Microsoft PowerPoint.app",
            "photoshop": "/Applications/Adobe Photoshop 2024/Adobe Photoshop.app",
            "illustrator": "/Applications/Adobe Illustrator 2024/Adobe Illustrator.app",
        }

        # Folder map
        self.folders = {
            "documents": f"{self.home}/Documents",
            "downloads": f"{self.home}/Downloads",
            "desktop": f"{self.home}/Desktop",
            "pictures": f"{self.home}/Pictures",
            "music folder": f"{self.home}/Music",
            "my music": f"{self.home}/Music",
            "movies": f"{self.home}/Movies",
            "my movies": f"{self.home}/Movies",
            "applications": "/Applications",
            "apps": "/Applications",
            "home": self.home,
            "my home": self.home,
        }

    def process(self, text):
        """Process any command and return response."""
        t = text.lower().strip()
        now = self.dt.datetime.now()

        # ---- TIME ----
        if any(w in t for w in ["what time", "time is it", "current time", "tell me the time", "what's the time"]):
            return f"The time is {now.strftime('%I:%M %p')}"

        # ---- DATE ----
        if any(w in t for w in ["what date", "today's date", "what day", "what's the date", "what is today"]):
            return f"Today is {now.strftime('%A, %B %d, %Y')}"

        # ---- JOKES ----
        if any(w in t for w in ["joke", "funny", "make me laugh", "tell me something funny"]):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "What's a computer's favorite snack? Microchips.",
                "Why did the computer go to the doctor? It had a virus.",
                "How does a computer get drunk? It takes screenshots.",
                "Why was the computer cold? It left its Windows open.",
                "What do you call a computer that sings? A Dell.",
                "Why do Java developers wear glasses? Because they can't C sharp.",
                "There are only 10 types of people in the world: those who understand binary and those who don't.",
                "A SQL query walks into a bar, sees two tables and asks: Can I join you?",
                "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
                "What's a robot's favorite type of music? Heavy metal.",
                "Why do robots never get tired? They're always recharged.",
            ]
            import random
            return random.choice(jokes)

        # ---- GREETINGS ----
        if any(w in t for w in ["hello", "hi ", "hey ", "how are you", "good morning", "good evening", "good afternoon", "good night"]):
            if "morning" in t:
                return "Good morning! Hope you have a productive day."
            elif "evening" in t:
                return "Good evening! How can I help?"
            elif "night" in t:
                return "Good night! Sleep well."
            elif "how are you" in t:
                return "I'm doing great, thank you! All systems operational."
            else:
                return "Hello! How can I help you?"

        # ---- WHO ARE YOU ----
        if any(w in t for w in ["who are you", "your name", "what are you", "tell me about yourself"]):
            return "I am JARVIS, Just A Rather Very Intelligent System. Your personal AI assistant."

        # ---- WHO MADE YOU ----
        if any(w in t for w in ["who made you", "who created you", "who built you", "your creator"]):
            return "I was created by Yash, a talented developer."

        # ---- THANKS ----
        if any(w in t for w in ["thank", "thanks", "appreciate"]):
            return "You're welcome! Always happy to help."

        # ---- CAPABILITIES ----
        if any(w in t for w in ["what can you do", "help", "capabilities", "features", "commands"]):
            return "I can open apps, tell time, jokes, control volume, WiFi, find files, calculate, and much more. Just ask!"

        # ---- OPEN APP ----
        if "open" in t:
            for name, path in self.folders.items():
                if name in t:
                    subprocess.Popen(["open", path])
                    return f"Opening {name}"

            for name, path in self.apps.items():
                if name in t:
                    subprocess.Popen(["open", path])
                    return f"Opening {name}"

            target = t.replace("open", "").strip()
            if target:
                subprocess.Popen(["open", target])
                return f"Opening {target}"

        # ---- CLOSE/QUIT ----
        if any(w in t for w in ["close", "quit", "exit", "stop"]):
            return "I can't close myself, but you can press Command Q to quit any app."

        # ---- VOLUME ----
        if any(w in t for w in ["volume up", "turn up", "louder", "increase volume"]):
            subprocess.Popen(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
            return "Volume increased"

        if any(w in t for w in ["volume down", "turn down", "quieter", "decrease volume", "lower volume"]):
            subprocess.Popen(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
            return "Volume decreased"

        if any(w in t for w in ["mute", "silence", "volume mute"]):
            subprocess.Popen(["osascript", "-e", "set volume with output muted"])
            return "Muted"

        if any(w in t for w in ["unmute", "unmute sound", "volume unmute"]):
            subprocess.Popen(["osascript", "-e", "set volume without output muted"])
            return "Unmuted"

        if "what volume" in t or "volume level" in t or "current volume" in t:
            result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
            vol = result.stdout.strip()
            return f"Volume is at {vol} percent"

        # ---- WIFI ----
        if any(w in t for w in ["wifi on", "turn on wifi", "enable wifi", "connect wifi"]):
            subprocess.Popen(["networksetup", "-setairportpower", "en0", "on"])
            return "WiFi turned on"

        if any(w in t for w in ["wifi off", "turn off wifi", "disable wifi"]):
            subprocess.Popen(["networksetup", "-setairportpower", "en0", "off"])
            return "WiFi turned off"

        # ---- BRIGHTNESS ----
        if any(w in t for w in ["brightness up", "brighter", "increase brightness", "screen brighter"]):
            subprocess.Popen(["brightness", "1"])
            return "Brightness at maximum"

        if any(w in t for w in ["brightness down", "dimmer", "decrease brightness", "screen dimmer"]):
            subprocess.Popen(["brightness", "0.5"])
            return "Brightness at 50 percent"

        # ---- CALCULATOR ----
        if any(w in t for w in ["calculate", "math", "what is", "what's"]):
            expr = t
            for word in ["calculate", "math", "what is", "what's", "compute"]:
                expr = expr.replace(word, "")
            expr = expr.strip()

            # Convert words to operators
            expr = expr.replace("x", "*").replace("times", "*").replace("multiplied by", "*")
            expr = expr.replace("plus", "+").replace("add", "+").replace("added to", "+")
            expr = expr.replace("minus", "-").replace("subtract", "-").replace("take away", "-")
            expr = expr.replace("divided by", "/").replace("over", "/").replace("divide", "/")
            expr = expr.replace("power", "**").replace("to the power of", "**").replace("squared", "**2").replace("cubed", "**3")

            try:
                result = eval(expr.replace("x", "*"))
                return f"The answer is {result}"
            except:
                return "Could not calculate that. Try: calculate 2 plus 2"

        # ---- RANDOM NUMBER ----
        if any(w in t for w in ["random number", "random", "give me a number"]):
            import random
            nums = [int(x) for x in t.split() if x.isdigit()]
            if len(nums) >= 2:
                result = random.randint(nums[0], nums[1])
                return f"Random number between {nums[0]} and {nums[1]}: {result}"
            else:
                result = random.randint(1, 100)
                return f"Random number: {result}"

        # ---- SPELL ----
        if t.startswith("spell"):
            word = t.replace("spell", "").replace("the word", "").strip()
            if word:
                spelled = ", ".join(list(word))
                return f"{word} is spelled {spelled}"

        # ---- FIND FILES ----
        if any(w in t for w in ["find", "search", "look for", "where is"]):
            query = t
            for word in ["find", "search for", "search", "look for", "where is", "where's"]:
                query = query.replace(word, "")
            query = query.strip()
            if query:
                return f"Searching for {query}. You can check in Finder."

        # ---- WEATHER ----
        if "weather" in t:
            return "I can check weather. What city are you interested in?"

        # ---- REMINDERS ----
        if any(w in t for w in ["remind", "reminder", "set reminder"]):
            subprocess.Popen(["open", "-a", "Reminders"])
            return "Opening Reminders app for you."

        # ---- NOTES ----
        if any(w in t for w in ["take note", "note", "write down", "make a note"]):
            subprocess.Popen(["open", "-a", "Notes"])
            return "Opening Notes app. You can dictate your note."

        # ---- CALL ----
        if any(w in t for w in ["call", "facetime", "video call", "phone call"]):
            contact = t
            for word in ["call", "facetime", "video call", "phone call", "phone"]:
                contact = contact.replace(word, "").strip()
            if contact:
                subprocess.Popen(["open", "-a", "FaceTime"])
                return f"Opening FaceTime to call {contact}"
            else:
                subprocess.Popen(["open", "-a", "FaceTime"])
                return "Opening FaceTime"

        # ---- MESSAGE ----
        if any(w in t for w in ["message", "text", "send message", "send text"]):
            contact = t
            for word in ["message", "text", "send message", "send text", "send"]:
                contact = contact.replace(word, "").strip()
            if contact:
                subprocess.Popen(["open", "-a", "Messages"])
                return f"Opening Messages to text {contact}"
            else:
                subprocess.Popen(["open", "-a", "Messages"])
                return "Opening Messages"

        # ---- BROWSER ----
        if any(w in t for w in ["browse", "google", "search the web", "look up"]):
            query = t
            for word in ["browse", "google", "search the web", "look up", "search for"]:
                query = query.replace(word, "").strip()
            if query:
                import urllib.parse
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                subprocess.Popen(["open", url])
                return f"Searching Google for {query}"
            else:
                subprocess.Popen(["open", "-a", "Google Chrome"])
                return "Opening Google Chrome"

        # ---- YOUTUBE ----
        if "youtube" in t:
            query = t.replace("youtube", "").replace("search", "").replace("play", "").strip()
            if query:
                import urllib.parse
                url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                subprocess.Popen(["open", url])
                return f"Searching YouTube for {query}"
            else:
                subprocess.Popen(["open", "https://www.youtube.com"])
                return "Opening YouTube"

        # ---- SHUTDOWN ----
        if any(w in t for w in ["shutdown", "shut down", "turn off"]):
            return "Say 'confirm shutdown' to shut down in 60 seconds."

        if "confirm shutdown" in t:
            subprocess.Popen(["sudo", "shutdown", "-h", "+1"])
            return "Shutting down in 1 minute."

        # ---- RESTART ----
        if any(w in t for w in ["restart", "reboot"]):
            return "Say 'confirm restart' to restart in 60 seconds."

        if "confirm restart" in t:
            subprocess.Popen(["sudo", "shutdown", "-r", "+1"])
            return "Restarting in 1 minute."

        # ---- SLEEP ----
        if any(w in t for w in ["sleep", "go to sleep", "lock screen"]):
            subprocess.Popen(["pmset", "displaysleepnow"])
            return "Going to sleep"

        # ---- CANCEL ----
        if any(w in t for w in ["cancel", "nevermind", "never mind", "forget it"]):
            subprocess.Popen(["sudo", "shutdown", "-c"])
            return "Cancelled"

        # ---- SYSTEM INFO ----
        if any(w in t for w in ["system info", "computer info", "specs", "what are my specs", "about this mac"]):
            subprocess.Popen(["open", "-a", "System Information"])
            return "Opening System Information"

        # ---- SCREENSHOT ----
        if any(w in t for w in ["screenshot", "take screenshot", "screen capture"]):
            subprocess.Popen(["screencapture", "-x", f"{self.home}/Desktop/screenshot.png"])
            return "Screenshot saved to Desktop"

        # ---- DEFAULT - ALWAYS RESPOND ----
        return f"I heard '{text}'. I'm still learning. Try asking me to open an app, tell a joke, or check the time."


# ============================================================
# SIRI-LIKE OVERLAY
# ============================================================
class CircleOverlay:
    """Small glowing circle that appears at bottom of screen."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.0)  # Start invisible
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        # Size
        self.W = 400
        self.H = 140

        # Position bottom center
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.W) // 2
        y = sh - self.H - 60
        self.root.geometry(f"{self.W}x{self.H}+{x}+{y}")

        # Main container
        self.container = tk.Frame(self.root, bg="#0a0a1a", bd=0, highlightthickness=1, highlightbackground="#00D4FF")
        self.container.pack(fill=tk.BOTH, expand=True)

        # Left: animated circle
        self.canvas = tk.Canvas(self.container, width=80, height=80, bg="#0a0a1a", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=(20, 15), pady=30)

        # Draw concentric circles
        self.rings = []
        colors = ["#00D4FF", "#00BFFF", "#0099CC", "#007799"]
        sizes = [(0, 70), (8, 62), (16, 54), (24, 46)]
        for i, (c, (s, e)) in enumerate(zip(colors, sizes)):
            ring = self.canvas.create_oval(s, s, e, e, outline=c, width=2, fill="")
            self.rings.append(ring)

        # Center dot
        self.center = self.canvas.create_oval(30, 30, 50, 50, fill="#00D4FF", outline="#00FFFF", width=2)

        # Right: text area
        self.text_frame = tk.Frame(self.container, bg="#0a0a1a")
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=15)

        # Status
        self.status_font = tkfont.Font(family="Helvetica Neue", size=11, weight="bold")
        self.status = tk.Label(self.text_frame, text=LOGO, font=self.status_font, fg="#00D4FF", bg="#0a0a1a", anchor="w")
        self.status.pack(fill=tk.X)

        # Message
        self.msg_font = tkfont.Font(family="Helvetica Neue", size=13)
        self.msg = tk.Label(self.text_frame, text="", font=self.msg_font, fg="#ffffff", bg="#0a0a1a", anchor="w", wraplength=260)
        self.msg.pack(fill=tk.X, pady=(5, 0))

        # Animation state
        self.phase = 0
        self.anim_id = None
        self.visible = False
        self.alpha = 0.0

    def show(self, message="Listening..."):
        """Show the overlay with fade-in."""
        self.msg.config(text=message)
        self.status.config(text=LOGO, fg="#00D4FF")
        self.visible = True
        self.alpha = 0.0
        self._fade_in()
        self._animate()

    def hide(self):
        """Hide with fade-out."""
        self._fade_out()

    def set_status(self, text, color="#00D4FF"):
        self.status.config(text=text, fg=color)

    def set_message(self, text):
        self.msg.config(text=text)

    def _fade_in(self):
        if self.alpha < 0.95 and self.visible:
            self.alpha += 0.1
            self.root.attributes("-alpha", self.alpha)
            self.root.after(20, self._fade_in)
        else:
            self.root.attributes("-alpha", 0.95)

    def _fade_out(self):
        if self.alpha > 0:
            self.alpha -= 0.1
            self.root.attributes("-alpha", self.alpha)
            self.root.after(20, self._fade_out)
        else:
            self.root.withdraw()
            self.visible = False

    def _animate(self):
        """Pulsing circle animation."""
        if not self.visible:
            return

        self.phase += 0.12
        if self.phase > math.pi * 2:
            self.phase = 0

        # Pulse intensity
        intensity = (math.sin(self.phase) + 1) / 2

        # Update rings
        for i, ring in enumerate(self.rings):
            offset = i * 0.3
            pulse = (math.sin(self.phase + offset) + 1) / 2
            brightness = int(180 + pulse * 75)
            color = f"#{brightness:02x}{brightness + 30:02x}ff"
            self.canvas.itemconfig(ring, outline=color)

        # Update center
        center_bright = int(200 + intensity * 55)
        self.canvas.itemconfig(self.center, fill=f"#{center_bright:02x}{center_bright + 30:02x}ff")

        self.anim_id = self.root.after(50, self._animate)

    def run(self):
        self.root.mainloop()


# ============================================================
# AUDIO ENGINE
# ============================================================
class Ears:
    """Listen for wake word and commands."""

    def __init__(self, overlay, brain):
        self.overlay = overlay
        self.brain = brain
        self.active = False
        self.processing = False

    def start(self):
        """Start listening thread."""
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def _loop(self):
        """Main listen loop."""
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except ImportError as e:
            print(f"Missing: {e}")
            print("pip3 install sounddevice vosk numpy")
            return

        # Load model
        model_dir = Path.home() / ".cache" / "vosk" / "vosk-model-small-en-us-0.15"
        if not model_dir.exists():
            print("Downloading speech model...")
            self._download(model_dir)

        try:
            model = Model(str(model_dir))
        except Exception as e:
            print(f"Model error: {e}")
            return

        rec = KaldiRecognizer(model, 16000)
        q = queue.Queue()

        def cb(indata, frames, time_info, status):
            q.put(bytes(indata))

        stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=cb)
        stream.start()
        print("Listening for 'Hey Jarvis'...")

        while True:
            data = q.get()

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()

                if text:
                    # Check wake word
                    if any(w in text for w in WAKE_WORDS):
                        self._wake(text)
            else:
                partial = json.loads(rec.PartialResult()).get("partial", "").lower()
                if any(w in partial for w in WAKE_WORDS):
                    if not self.active:
                        self._wake(partial)

    def _wake(self, full_text=""):
        """Handle wake word."""
        if self.processing:
            return

        self.active = True
        print("Wake word detected!")
        self._beep()
        self.overlay.show("Listening...")

        # Extract command
        cmd = full_text
        for w in WAKE_WORDS:
            cmd = cmd.replace(w, "").strip()

        if cmd and len(cmd) > 2:
            self._respond(cmd)
        else:
            self._listen_cmd()

    def _listen_cmd(self):
        """Listen for command after wake word."""
        threading.Thread(target=self._cmd_listener, daemon=True).start()

    def _cmd_listener(self):
        """Short listen for command."""
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except:
            return

        model_dir = Path.home() / ".cache" / "vosk" / "vosk-model-small-en-us-0.15"
        if not model_dir.exists():
            return

        model = Model(str(model_dir))
        rec = KaldiRecognizer(model, 16000)
        q = queue.Queue()

        def cb(indata, frames, time_info, status):
            q.put(bytes(indata))

        stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=cb)
        stream.start()

        start = time.time()
        while time.time() - start < LISTEN_TIMEOUT:
            data = q.get()

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()
                if text and len(text) > 2:
                    stream.stop()
                    stream.close()
                    self._respond(text)
                    return

        # Timeout
        stream.stop()
        stream.close()
        self.overlay.set_message("No command heard")
        time.sleep(1)
        self.overlay.hide()
        self.active = False

    def _respond(self, command):
        """Process command and respond."""
        self.processing = True
        self.overlay.set_status("Thinking...", "#FFC84D")
        self.overlay.set_message(f'"{command}"')

        def process():
            try:
                response = self.brain.process(command)
                self.overlay.set_status(LOGO, "#4DFF7C")
                self.overlay.set_message(response)
                self._speak(response)
                time.sleep(3)
                self.overlay.hide()
            except Exception as e:
                self.overlay.set_status("Error", "#FF4D4D")
                self.overlay.set_message(str(e))
                time.sleep(2)
                self.overlay.hide()
            finally:
                self.processing = False
                self.active = False

        threading.Thread(target=process, daemon=True).start()

    def _speak(self, text):
        """Speak with smooth voice."""
        try:
            # Clean text for TTS
            clean = text.replace('"', '').replace("'", "").replace("\n", " ")
            # Use macOS Samantha voice with natural rate
            subprocess.run(
                ["osascript", "-e", f'say "{clean}" using voice "{VOICE}" rate {VOICE_RATE}'],
                timeout=15,
                capture_output=True
            )
        except:
            try:
                subprocess.run(["say", text], timeout=15, capture_output=True)
            except:
                pass

    def _beep(self):
        """Play activation sound."""
        try:
            subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    def _download(self, path):
        """Download vosk model."""
        import urllib.request, zipfile
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, "/tmp/vosk.zip")
        with zipfile.ZipFile("/tmp/vosk.zip") as z:
            z.extractall(str(path.parent))
        os.remove("/tmp/vosk.zip")
        print("Model ready!")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 50)
    print("  J.A.R.V.I.S - Siri-Like Assistant")
    print("=" * 50)
    print()
    print("  Say 'Hey Jarvis' to activate!")
    print("  Commands: open apps, time, jokes, volume, wifi...")
    print("  Press Ctrl+C to quit")
    print()

    brain = Brain()
    overlay = CircleOverlay()
    ears = Ears(overlay, brain)

    # Start listening
    ears.start()

    # Start UI (main thread)
    try:
        overlay.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
