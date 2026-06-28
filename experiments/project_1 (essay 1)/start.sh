#!/usr/bin/env bash
set -e

# Kill existing processes on used ports
kill -9 $(lsof -t -i:8000) 2>/dev/null || true
kill -9 $(lsof -t -i:3000) 2>/dev/null || true

# Start frontend
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_1/frontend
npm install
npm run dev &
FRONTEND_PID=$!

# Start backend
cd /home/mahdi/Desktop/Work/dev/product-owner-ai/experiments/project_1/dev
pip install -r requirements.txt -q 2>/dev/null || true
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo 'Services started:'
echo '  Backend : http://localhost:8000'
echo '  Frontend: http://localhost:3000'

wait $BACKEND_PID
