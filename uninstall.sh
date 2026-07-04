#!/bin/bash
# ============================================
# JARVIS AI - Uninstall Script
# Removes the auto-start launch agent
# ============================================

echo "Uninstalling JARVIS Listener..."

PLIST="$HOME/Library/LaunchAgents/com.jarvis.listener.plist"

# Unload the agent
launchctl unload "$PLIST" 2>/dev/null
echo "  Agent unloaded"

# Remove the plist
rm -f "$PLIST"
echo "  Plist removed"

# Kill any running instances
pkill -f jarvis_listener.py 2>/dev/null
echo "  Listener stopped"

echo ""
echo "JARVIS Listener uninstalled."
echo "You can still use JARVIS by opening: http://localhost:8000/jarvis.html"
