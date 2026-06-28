#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Kill only the ports this project uses (avoid touching 8000 = product owner AI)
kill -9 $(lsof -t -i:8765) 2>/dev/null || true
kill -9 $(lsof -t -i:3000) 2>/dev/null || true

# Start frontend
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

# Start backend (port 8765 — avoids conflict with product owner AI on 8000)
cd dev
pip install -r requirements.txt -q 2>/dev/null || true
uvicorn main:app --reload --port 8765 &
BACKEND_PID=$!
cd ..

echo 'Services started:'
echo '  Backend : http://localhost:8765'
echo '  Frontend: http://localhost:3000'

wait $BACKEND_PID
