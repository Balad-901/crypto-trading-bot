# tools/backtester.py

import json
import os
import matplotlib.pyplot as plt
from tabulate import tabulate

def load_decisions(path="logs/decisions.json"):
    if not os.path.exists(path):
        print("⚠️ No decisions.json file found.")
        return []

    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def replay_trades(decisions):
    if not decisions:
        print("⚠️ No decisions to replay.")
        return []

    results = []
    for entry in decisions:
        results.append([
            entry.get("symbol", "N/A"),
            entry.get("signal", "N/A"),
            entry.get("confidence", 0),
            entry.get("timeframe", "N/A"),
            entry.get("summary", "N/A")[:60] + "...",
        ])

    print("\n📊 Backtest Replay:")
    print(tabulate(results, headers=["Symbol", "Signal", "Confidence", "Timeframe", "Summary"], tablefmt="fancy_grid"))
    return decisions

def plot_pnl(decisions):
    pnl = 0.0
    pnl_curve = []
    for i, entry in enumerate(decisions):
        # Simulate PnL gain/loss (for now: +10% on buy, -5% on sell)
        if entry.get("signal") == "buy":
            pnl += 0.10
        elif entry.get("signal") == "sell":
            pnl -= 0.05
        pnl_curve.append(pnl)

    plt.plot(pnl_curve, marker='o')
    plt.title("Simulated PnL Over Time")
    plt.xlabel("Trade #")
    plt.ylabel("Cumulative PnL")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    data = load_decisions()
    replayed = replay_trades(data)
    plot_pnl(replayed)
