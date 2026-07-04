#!/bin/bash
# ============================================
# JARVIS Siri-Like Assistant - Start Script
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting JARVIS Siri-Like Assistant..."
echo "Say 'Hey Jarvis' to activate the circle!"
echo "Press Ctrl+C to stop"
echo ""

python3 "$SCRIPT_DIR/jarvis_siri.py"
