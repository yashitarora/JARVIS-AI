#!/bin/bash
# ============================================
# JARVIS AI - Start Listener
# Run this to start the always-on listener
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting JARVIS Listener..."
echo "Say 'Hey Jarvis' to activate!"
echo "Press Ctrl+C to stop"
echo ""

python3 "$SCRIPT_DIR/jarvis_listener.py"
