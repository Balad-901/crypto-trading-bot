# scheduler/auto_memory_loop.py

import time
from datetime import datetime
import os
import subprocess

SYMBOLS = ["BTC", "ETH", "ADA", "XRP", "ARB", "HBAR", "SOL"]
LOOP_HOURS = 1  # how often to run (every 1 hour)

def run(label, command):
    print(f"\n⏳ [{datetime.utcnow().isoformat()}] Running: {label}")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Finished: {label}")
    except Exception as e:
        print(f"❌ Error in {label}: {e}")

def loop():
    while True:
        for symbol in SYMBOLS:
            run(f"Research {symbol}", f"python3 research/runner.py {symbol}")
            time.sleep(15)  # short delay between symbols to avoid rate limits

        run("Generate Pattern Summary", "python3 llm/pattern_memory.py")
        run("Update Biases", "python3 llm/update_biases.py")

        now = datetime.now().strftime("%Y-%m-%d_%H%M")
        print(f"🕒 Sleeping {LOOP_HOURS}h... ⏸ [{now}]")
        time.sleep(LOOP_HOURS * 60 * 60)

if __name__ == "__main__":
    loop()
