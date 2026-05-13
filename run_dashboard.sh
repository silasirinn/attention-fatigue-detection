#!/bin/bash

# Terminate on error
set -e

echo "Starting CogniSense AI Backend (FastAPI)..."
# Check if uvicorn is running and kill it (optional)
pkill -f "uvicorn api:app" || true

# Use conda python if available to avoid Python 3.13 / mediapipe issues
if [ -x "/opt/anaconda3/bin/python" ]; then
    PYTHON_CMD="/opt/anaconda3/bin/python"
    echo "Using Anaconda Python: $PYTHON_CMD"
else
    PYTHON_CMD="python3"
    echo "Using System Python: $PYTHON_CMD"
fi

# Start backend in background
$PYTHON_CMD api.py &
BACKEND_PID=$!

echo "Starting CogniSense AI Dashboard (Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "========================================="
echo "Dashboard is running!"
echo "Backend WS: ws://127.0.0.1:8000/ws"
echo "Frontend UI: http://localhost:5173"
echo "========================================="
echo "Press Ctrl+C to stop both servers."

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
