#!/bin/bash
# ============================================
# JARVIS Siri-Like Assistant - Install
# ============================================

echo "========================================="
echo "  JARVIS Siri-Like Assistant"
echo "========================================="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_DST="$HOME/Library/LaunchAgents/com.jarvis.siri.plist"

echo ""
echo "[1/4] Installing dependencies..."
pip3 install sounddevice vosk numpy 2>&1 | tail -3

echo ""
echo "[2/4] Making scripts executable..."
chmod +x "$SCRIPT_DIR/jarvis_siri.py"
chmod +x "$SCRIPT_DIR/start_siri.sh"

echo ""
echo "[3/4] Installing launch agent..."
cp "$SCRIPT_DIR/com.jarvis.siri.plist" "$PLIST_DST" 2>/dev/null || \
cp "$SCRIPT_DIR/jarvis_siri.plist" "$PLIST_DST" 2>/dev/null
launchctl unload "$PLIST_DST" 2>/dev/null
launchctl load "$PLIST_DST"
echo "  Agent installed!"

echo ""
echo "[4/4] Downloading speech model (first time only)..."
python3 -c "
from vosk import Model
import os
model_path = os.path.expanduser('~/.cache/vosk/vosk-model-small-en-us-0.15')
if not os.path.exists(model_path):
    print('Downloading model...')
    import urllib.request, zipfile
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    url = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
    urllib.request.urlretrieve(url, '/tmp/vosk-model.zip')
    with zipfile.ZipFile('/tmp/vosk-model.zip') as z:
        z.extractall(os.path.dirname(model_path))
    os.remove('/tmp/vosk-model.zip')
    print('Model downloaded!')
else:
    print('Model already exists')
" 2>&1

echo ""
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "  Say 'Hey Jarvis' anywhere near your"
echo "  laptop and a circle will appear!"
echo ""
echo "  To start now:"
echo "    $SCRIPT_DIR/start_siri.sh"
echo ""
echo "  To stop:"
echo "    launchctl unload $PLIST_DST"
echo ""
echo "  To uninstall:"
echo "    launchctl unload $PLIST_DST"
echo "    rm $PLIST_DST"
echo "========================================="
