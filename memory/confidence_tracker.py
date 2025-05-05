import json
import os

CONFIDENCE_FILE = "memory/confidence_learning.json"

def load_confidence_data():
    if not os.path.exists(CONFIDENCE_FILE):
        return {}
    with open(CONFIDENCE_FILE, "r") as f:
        return json.load(f)

def save_confidence_data(data):
    with open(CONFIDENCE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_confidence(symbol, timeframe, signal, confidence, result=None):
    data = load_confidence_data()
    if symbol not in data:
        data[symbol] = {}
    if timeframe not in data[symbol]:
        data[symbol][timeframe] = {}
    if signal not in data[symbol][timeframe]:
        data[symbol][timeframe][signal] = {
            "count": 0,
            "avg_confidence": 0.0,
            "wins": 0,
            "losses": 0
        }

    entry = data[symbol][timeframe][signal]
    entry["count"] += 1
    entry["avg_confidence"] = round((entry["avg_confidence"] * (entry["count"] - 1) + confidence) / entry["count"], 2)

    if result == "win":
        entry["wins"] += 1
    elif result == "loss":
        entry["losses"] += 1

    save_confidence_data(data)

def get_learned_boost(symbol, timeframe, signal):
    data = load_confidence_data()
    try:
        stats = data[symbol][timeframe][signal]
        win_rate = stats["wins"] / max(1, stats["wins"] + stats["losses"])
        return round(win_rate * 0.2, 3)  # max +0.2 boost
    except:
        return 0.0
