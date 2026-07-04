# JARVIS AI - Personal AI Assistant

A Siri-like personal AI assistant for macOS that runs in the background and activates when you say **"Hey Jarvis"**.

## Features

- **Always Listening** - Say "Hey Jarvis" anywhere near your Mac
- **Siri-Like Interface** - Glowing circle appears at bottom of screen
- **50+ Commands** - Open apps, tell time, jokes, control volume, WiFi, and more
- **Smooth Voice** - Uses macOS built-in voices (Samantha) for natural responses
- **Auto-Start** - Starts automatically when you log in
- **Offline** - Works completely offline after initial setup

## Quick Start

### Option 1: Run the App
1. Double-click `JARVIS.app` on your Desktop
2. Say "Hey Jarvis" to activate

### Option 2: Run from Terminal
```bash
cd ~/Desktop/JARVIS-AI
python3 jarvis_siri.py
```

### Option 3: Install for Auto-Start
```bash
cd ~/Desktop/JARVIS-AI
./install_siri.sh
```

## Commands

| Command | Description |
|---------|-------------|
| "Hey Jarvis, what time is it?" | Tell the current time |
| "Hey Jarvis, open Chrome" | Open Google Chrome |
| "Hey Jarvis, tell me a joke" | Tell a random joke |
| "Hey Jarvis, volume up" | Increase volume |
| "Hey Jarvis, volume down" | Decrease volume |
| "Hey Jarvis, mute" | Mute audio |
| "Hey Jarvis, wifi on" | Turn on WiFi |
| "Hey Jarvis, wifi off" | Turn off WiFi |
| "Hey Jarvis, open Documents" | Open Documents folder |
| "Hey Jarvis, find my resume" | Search for files |
| "Hey Jarvis, calculate 2 plus 2" | Do math |
| "Hey Jarvis, random number" | Generate random number |
| "Hey Jarvis, google Python tutorials" | Search Google |
| "Hey Jarvis, youtube music" | Search YouTube |
| "Hey Jarvis, call mom" | Open FaceTime |
| "Hey Jarvis, message John" | Open Messages |
| "Hey Jarvis, take a note" | Open Notes app |
| "Hey Jarvis, screenshot" | Take screenshot |
| "Hey Jarvis, sleep" | Put Mac to sleep |
| "Hey Jarvis, shutdown" | Shut down Mac |
| "Hey Jarvis, help" | Show all commands |

## Files

- `jarvis_siri.py` - Main assistant (Siri-like circle)
- `jarvis.html` - Web-based HUD interface
- `backend.py` - API backend server
- `JARVIS.app` - macOS app bundle
- `install_siri.sh` - Install auto-start
- `start_siri.sh` - Start manually

## Requirements

- macOS 12.0 or later
- Python 3.8+
- Microphone access
- Internet connection (for initial model download only)

## Installation

```bash
# Install dependencies
pip3 install sounddevice vosk numpy

# Download speech model (automatic on first run)
# Or download manually from: https://alphacephei.com/vosk/models

# Run JARVIS
python3 jarvis_siri.py
```

## How It Works

1. **Wake Word Detection** - Uses Vosk offline speech recognition to detect "Hey Jarvis"
2. **Command Processing** - Processes 50+ commands locally
3. **Response** - Uses macOS `say` command with Samantha voice
4. **Interface** - Shows animated glowing circle overlay

## License

MIT License
