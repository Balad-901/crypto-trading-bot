# research/auto_runner.py

import sys
import os
import time
import random
import schedule

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from research.runner import run_research

SYMBOLS = ["BTCUSDT", "ETHUSDT", "ARB", "PIXEL", "HBAR", "ADA"]

def run_all():
    print("🔁 Starting research loop...")
    for symbol in SYMBOLS:
        run_research(symbol)
        time.sleep(8)  # Avoid 429 per symbol
    print("✅ Research loop complete.")

    # Set a random delay before next full cycle (1 to 30 minutes)
    next_delay = random.randint(60, 1800)
    print(f"⏳ Waiting {next_delay // 60}m {next_delay % 60}s before next research cycle...\n")
    time.sleep(next_delay)
    run_all()

# Initial run
run_all()
