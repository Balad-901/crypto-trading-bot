# scripts/backtest_replay.py

import sys
import os
import json

# ✅ Add root path so we can import llm modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.pattern_memory import update_pattern_memory

# Paths
DECISIONS_PATH = "memory/decisions.json"
SENTIMENT_PATH = "memory/sentiment_history.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def replay():
    print("📦 Loading historical data...")
    decisions = load_json(DECISIONS_PATH)
    sentiment = load_json(SENTIMENT_PATH)

    combined = []
    for symbol in sentiment:
        for entry in sentiment[symbol]:
            combined.append({
                "symbol": symbol,
                "timestamp": entry.get("timestamp"),
                "sentiment": entry.get("score"),
            })

    print(f"📚 Replaying {len(combined)} sentiment entries into memory...")

    for entry in combined:
        update_pattern_memory(
            symbol=entry["symbol"],
            confidence=entry["sentiment"],
            timestamp=entry["timestamp"],
            reason="(historical replay)"
        )

    print("✅ Historical replay complete.")

if __name__ == "__main__":
    replay()
