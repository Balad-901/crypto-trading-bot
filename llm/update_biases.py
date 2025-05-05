# llm/update_biases.py

import json
import os
from datetime import datetime

bias_path = "memory/biases.json"
trade_log_path = "logs/trades.json"

def load_biases():
    if not os.path.exists(bias_path):
        return {}
    with open(bias_path, "r") as f:
        return json.load(f)

def save_biases(biases):
    with open(bias_path, "w") as f:
        json.dump(biases, f, indent=2)

def load_trades():
    if not os.path.exists(trade_log_path):
        return []
    with open(trade_log_path, "r") as f:
        return json.load(f)

def update_from_trades(biases):
    trades = load_trades()
    for trade in trades:
        pnl = trade.get("pnl", 0)
        active_topics = trade.get("active_biases", {})
        for topic, weight in active_topics.items():
            if topic not in biases:
                biases[topic] = 0.5  # neutral start
            adjustment = 0.05 if pnl > 0 else -0.05
            biases[topic] += adjustment * weight
            biases[topic] = max(0.0, min(1.0, biases[topic]))  # keep between 0-1
    return biases

def main():
    print("🔁 Updating long-term topic biases...")
    biases = load_biases()
    biases = update_from_trades(biases)
    save_biases(biases)
    print(f"✅ Biases updated and saved to {bias_path}")

if __name__ == "__main__":
    main()
