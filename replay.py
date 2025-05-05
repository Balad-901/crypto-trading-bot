# replay.py

import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

RESULTS_FILE = "logs/results.json"

def load_results():
    if not os.path.exists(RESULTS_FILE):
        print("No results found.")
        return []
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)

def replay_trades():
    results = load_results()
    pnl = 0
    balance = [0]
    labels = []
    wins = 0
    losses = 0

    for i, trade in enumerate(results):
        pnl += trade["pnl"]
        balance.append(round(pnl, 2))
        date_label = f"T{i+1}"
        labels.append(date_label)
        if trade["result"] == "win":
            wins += 1
        else:
            losses += 1

    # Plot PnL curve
    plt.figure(figsize=(12, 5))
    plt.plot(balance, marker="o", linewidth=2)
    plt.title("📈 Trading Bot PnL Over Time")
    plt.xlabel("Trade")
    plt.ylabel("Net PnL ($)")
    plt.xticks(range(len(labels)), labels, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.axhline(0, color="black", linestyle="--")
    plt.show()

    print("=== REPLAY REPORT ===")
    print(f"Total Trades: {len(results)}")
    print(f"Wins:         {wins}")
    print(f"Losses:       {losses}")
    print(f"Final Net PnL: ${pnl:.2f}")

if __name__ == "__main__":
    replay_trades()
