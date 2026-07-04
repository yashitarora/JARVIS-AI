#!/usr/bin/env python3
"""
JARVIS Background Listener
Always listens for "Hey Jarvis" and opens JARVIS when detected.
Uses sounddevice + vosk for audio capture and speech recognition.
"""

import os
import sys
import time
import subprocess
import signal
import logging
import json
import queue
from pathlib import Path

# ============================================================
# Configuration
# ============================================================
JARVIS_URL = "http://localhost:8000/jarvis.html"
JARVIS_BACKEND = "http://localhost:8000/health"
JARVIS_DIR = Path(__file__).parent
LOG_FILE = Path("/tmp/jarvis-listener.log")
PID_FILE = Path("/tmp/jarvis-listener.pid")

# ============================================================
# Setup Logging
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("jarvis-listener")

# ============================================================
# Import audio libraries
# ============================================================
try:
    import sounddevice as sd
    import numpy as np
    HAS_AUDIO = True
except ImportError as e:
    HAS_AUDIO = False
    log.warning(f"sounddevice not available: {e}")

try:
    from vosk import Model, KaldiRecognizer
    HAS_VOSK = True
except ImportError as e:
    HAS_VOSK = False
    log.warning(f"vosk not available: {e}")


def write_pid():
    PID_FILE.write_text(str(os.getpid()))


def cleanup(signum=None, frame=None):
    log.info("Listener shutting down...")
    if PID_FILE.exists():
        PID_FILE.unlink()
    sys.exit(0)


def is_jarvis_running():
    try:
        import urllib.request
        urllib.request.urlopen(JARVIS_BACKEND, timeout=2)
        return True
    except:
        return False


def start_jarvis_backend():
    if is_jarvis_running():
        log.info("JARVIS backend already running")
        return True

    log.info("Starting JARVIS backend...")
    backend_script = JARVIS_DIR / "backend.py"
    if backend_script.exists():
        subprocess.Popen(
            [sys.executable, str(backend_script)],
            cwd=str(JARVIS_DIR),
            stdout=open("/tmp/jarvis-ai.log", "w"),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        for i in range(10):
            time.sleep(1)
            if is_jarvis_running():
                log.info("JARVIS backend started successfully")
                return True
    return False


def open_jarvis_browser():
    log.info("Opening JARVIS in browser...")
    browsers = [
        ["open", "-a", "Google Chrome", JARVIS_URL],
        ["open", "-a", "Safari", JARVIS_URL],
        ["open", JARVIS_URL],
    ]
    for cmd in browsers:
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except:
            continue


def play_activation_sound():
    try:
        subprocess.Popen(
            ["afplay", "/System/Library/Sounds/Glass.aiff"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass


def listen_with_vosk():
    """Listen using sounddevice + vosk."""
    log.info("Initializing audio...")

    # Vosk model (small English model)
    model_path = Path.home() / ".cache" / "vosk" / "vosk-model-small-en-us-0.15"
    if not model_path.exists():
        log.info("Downloading Vosk model (first time only)...")
        import urllib.request
        import zipfile
        import io

        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        model_zip_path = Path.home() / ".cache" / "vosk"
        model_zip_path.mkdir(parents=True, exist_ok=True)

        try:
            log.info("Downloading from: " + model_url)
            urllib.request.urlretrieve(model_url, str(model_zip_path / "model.zip"))
            with zipfile.ZipFile(str(model_zip_path / "model.zip"), 'r') as zip_ref:
                zip_ref.extractall(str(model_zip_path))
            log.info("Model downloaded successfully")
        except Exception as e:
            log.error(f"Failed to download model: {e}")
            log.info("You can download manually from: https://alphacephei.com/vosk/models")
            return False

    log.info("Loading Vosk model...")
    model = Model(str(model_path))
    recognizer = KaldiRecognizer(model, 16000)
    log.info("Vosk model loaded")

    # Audio queue
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        if status:
            log.warning(f"Audio status: {status}")
        audio_queue.put(bytes(indata))

    # Open audio stream
    log.info("Opening microphone...")
    stream = sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    )

    stream.start()
    log.info("Listening for 'Hey Jarvis'... (speak to activate)")

    try:
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()

                if text:
                    log.info(f"Heard: {text}")

                    # Check for wake word
                    if "hey jarvis" in text or "hey jarvis" in text or "hey jarvis" in text:
                        log.info("WAKE WORD DETECTED!")
                        play_activation_sound()

                        # Extract command after wake word
                        command = text.replace("hey jarvis", "").replace("hey jarvis", "").strip()

                        # Start backend and open browser
                        start_jarvis_backend()
                        open_jarvis_browser()

                        if command:
                            log.info(f"Command: {command}")

                        time.sleep(3)  # Wait before listening again

            else:
                # Partial result
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "")
                if "hey jarvis" in partial_text.lower():
                    # Wake word detected in partial result too
                    pass

    except KeyboardInterrupt:
        log.info("Interrupted by user")
    finally:
        stream.stop()
        stream.close()


def listen_polling():
    """Fallback: just keep backend running."""
    log.info("Running in polling mode (no audio libraries)")
    log.info(f"JARVIS will be available at: {JARVIS_URL}")
    log.info("Press Ctrl+C to stop")

    start_jarvis_backend()

    while True:
        time.sleep(60)
        if not is_jarvis_running():
            start_jarvis_backend()


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    write_pid()
    log.info(f"JARVIS Listener started (PID: {os.getpid()})")

    # Check if another instance is running
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            if old_pid != os.getpid():
                try:
                    os.kill(old_pid, 0)
                    log.warning("Another instance running. Exiting.")
                    sys.exit(1)
                except OSError:
                    pass
        except:
            pass

    write_pid()

    # Start backend
    start_jarvis_backend()

    # Listen for wake word
    if HAS_AUDIO and HAS_VOSK:
        listen_with_vosk()
    else:
        log.warning("Audio libraries not available. Install with:")
        log.warning("  pip3 install sounddevice vosk numpy")
        listen_polling()


if __name__ == "__main__":
    main()
