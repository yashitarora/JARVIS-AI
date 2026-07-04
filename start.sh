#!/bin/bash
# JARVIS AI - Startup Script
# Kills any existing servers and starts fresh

echo "========================================="
echo "  JARVIS AI - Starting Up..."
echo "========================================="

# Kill existing processes on ports 8000 and 8080
echo "[1/4] Stopping existing servers..."
lsof -ti :8000 | xargs kill -9 2>/dev/null
lsof -ti :8080 | xargs kill -9 2>/dev/null
sleep 1

# Navigate to script directory
cd "$(dirname "$0")"

# Install requirements if needed
echo "[2/4] Checking requirements..."
pip3 install fastapi uvicorn psutil 2>/dev/null || pip install fastapi uvicorn psutil 2>/dev/null

# Start backend server
echo "[3/4] Starting JARVIS backend on port 8000..."
python3 backend.py > /tmp/jarvis-ai-backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# Check if backend started
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  Backend: OK (PID: $BACKEND_PID)"
else
    echo "  Backend: Starting... (may take a moment)"
fi

echo ""
echo "========================================="
echo "  JARVIS AI is ready!"
echo "========================================="
echo ""
echo "  Open in browser: http://localhost:8000/jarvis.html"
echo ""
echo "  Or open the file directly:"
echo "  file://$(pwd)/jarvis.html"
echo ""
echo "  Backend API: http://localhost:8000"
echo "  Health check: http://localhost:8000/health"
echo ""
echo "  To stop: kill $BACKEND_PID"
echo "========================================="

# Keep script running
wait $BACKEND_PID
