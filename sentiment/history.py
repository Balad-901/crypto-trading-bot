# sentiment/history.py

import os
import json
from datetime import datetime

HISTORY_FILE = "sentiment/sentiment_history.json"

def save_to_history(summary):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

        # Load old history if exists
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []

        # Append new record
        new_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "avg_sentiment": summary.get("avg_sentiment", {}),
            "volatility": summary.get("volatility", {})
        }
        history.append(new_entry)

        # Limit history to last 1000 entries to avoid unlimited growth
        history = history[-1000:]

        # Save updated history
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)

    except Exception as e:
        print(f"⚠️ Error saving sentiment history: {e}")

def load_history():
    try:
        if not os.path.exists(HISTORY_FILE):
            return []
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading sentiment history: {e}")
        return []
