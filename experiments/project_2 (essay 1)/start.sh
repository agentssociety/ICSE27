#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Kill existing processes on used ports
kill -9 $(lsof -t -i:8000) 2>/dev/null || true
kill -9 $(lsof -t -i:3000) 2>/dev/null || true

# Start frontend
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

# Start backend
cd dev
pip install -r requirements.txt -q 2>/dev/null || true
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo 'Services started:'
echo '  Backend : http://localhost:8000'
echo '  Frontend: http://localhost:3000'

wait $BACKEND_PID
