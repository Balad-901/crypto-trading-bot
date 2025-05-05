import json
import os

LEARNING_FILE = "memory/confidence_learning.json"

def load_learning_data():
    if not os.path.exists(LEARNING_FILE):
        return {}
    with open(LEARNING_FILE, "r") as f:
        return json.load(f)

def save_learning_data(data):
    with open(LEARNING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_learning(symbol, timeframe, confidence, result):
    key = f"{symbol}_{timeframe}"
    data = load_learning_data()
    if key not in data:
        data[key] = []

    entry = {"confidence": confidence, "result": result}
    data[key].append(entry)

    # Limit history length to avoid file bloat
    data[key] = data[key][-100:]

    save_learning_data(data)

def adjust_confidence(symbol, timeframe, confidence):
    key = f"{symbol}_{timeframe}"
    data = load_learning_data()
    if key not in data or not data[key]:
        return confidence  # no history yet

    history = data[key]
    avg_result = sum(x["result"] for x in history) / len(history)
    adjustment = (avg_result - 0.5) * 0.3  # scale adjustment factor

    adjusted = confidence + adjustment
    return max(0.0, min(1.0, round(adjusted, 4)))
