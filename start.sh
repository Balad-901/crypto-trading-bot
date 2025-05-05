#!/bin/bash
echo "✅ Starting crypto bot..."

# Run research loop in background
python3 scheduler/auto_memory_loop.py &

# Run FastAPI dashboard
uvicorn main:app --host 0.0.0.0 --port 10000
