#!/bin/bash
# ============================================
# JARVIS AI - Install Script
# Sets up always-on "Hey Jarvis" listener
# ============================================

echo "========================================="
echo "  JARVIS AI - Installation"
echo "========================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_SRC="$SCRIPT_DIR/com.jarvis.listener.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.jarvis.listener.plist"

# Step 1: Install Python dependencies
echo ""
echo "[1/5] Installing Python dependencies..."
pip3 install SpeechRecognition pyaudio fastapi uvicorn psutil 2>&1 | tail -3

# Step 2: Make scripts executable
echo ""
echo "[2/5] Making scripts executable..."
chmod +x "$SCRIPT_DIR/jarvis_listener.py"
chmod +x "$SCRIPT_DIR/start.sh"
chmod +x "$SCRIPT_DIR/backend.py"

# Step 3: Copy launch agent
echo ""
echo "[3/5] Installing launch agent..."
cp "$PLIST_SRC" "$PLIST_DST"
echo "  Installed: $PLIST_DST"

# Step 4: Unload existing agent (if any)
echo ""
echo "[4/5] Unloading existing agent..."
launchctl unload "$PLIST_DST" 2>/dev/null

# Step 5: Load the agent
echo ""
echo "[5/5] Loading launch agent..."
launchctl load "$PLIST_DST"
echo "  Agent loaded!"

# Verify
echo ""
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "  JARVIS will now start automatically"
echo "  when you log in to your Mac."
echo ""
echo "  To start NOW:"
echo "    python3 $SCRIPT_DIR/jarvis_listener.py"
echo ""
echo "  Or open browser to:"
echo "    http://localhost:8000/jarvis.html"
echo ""
echo "  To stop the listener:"
echo "    launchctl unload $PLIST_DST"
echo ""
echo "  To uninstall:"
echo "    launchctl unload $PLIST_DST"
echo "    rm $PLIST_DST"
echo "========================================="
