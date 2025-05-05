# memory/writer.py

import os
import json
from datetime import datetime

LOG_PATH = "logs/sentiment_history.json"

def save_memory_summary(symbol, summary, sentiment, topic, extra=None):
    os.makedirs("logs", exist_ok=True)

    entry = {
        "symbol": symbol,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary,
        "sentiment": sentiment,
        "topic": topic
    }

    if extra:
        entry.update(extra)

    if not os.path.exists(LOG_PATH):
        memory = {}

    else:
        with open(LOG_PATH, "r") as f:
            memory = json.load(f)

    if symbol not in memory:
        memory[symbol] = []

    memory[symbol].append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(memory, f, indent=2)

    print(f"💾 Saved memory for {symbol}")
