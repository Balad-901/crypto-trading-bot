# stats.py

import json
import os

RESULTS_FILE = "logs/results.json"

def load_results():
    if not os.path.exists(RESULTS_FILE):
        print("⚠️ No results.json file found.")
        return []
    with open(RESULTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Could not parse results.json")
            return []

def analyze_results(trades):
    total_trades = len(trades)
    wins = [t for t in trades if t["result"] == "win"]
    losses = [t for t in trades if t["result"] == "loss"]

    net_pnl = sum(t["pnl"] for t in trades)
    avg_return = sum(t["return_percent"] for t in trades) / total_trades if total_trades > 0 else 0

    best_trade = max(trades, key=lambda x: x["pnl"], default=None)
    worst_trade = min(trades, key=lambda x: x["pnl"], default=None)

    return {
        "total": total_trades,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round((len(wins) / total_trades) * 100, 2) if total_trades else 0,
        "net_pnl": round(net_pnl, 2),
        "avg_return": round(avg_return, 2),
        "best_trade": best_trade,
        "worst_trade": worst_trade
    }

def display_report(stats):
    print("===================================")
    print("  📊 TRADE PERFORMANCE REPORT")
    print("-----------------------------------")
    print(f" ✅ Total Trades:   {stats['total']}")
    print(f" 🎯 Wins:           {stats['wins']} ({stats['win_rate']}%)")
    print(f" ❌ Losses:         {stats['losses']}")
    print(f" 💰 Net PnL:        ${stats['net_pnl']}")
    print(f" 📈 Avg Return:     {stats['avg_return']}%")

    if stats["best_trade"]:
        print(f" 🚀 Best Trade:     +${stats['best_trade']['pnl']} ({stats['best_trade']['return_percent']}%)")
    if stats["worst_trade"]:
        print(f" 🔻 Worst Trade:    ${stats['worst_trade']['pnl']} ({stats['worst_trade']['return_percent']}%)")
    print("===================================")

if __name__ == "__main__":
    trades = load_results()
    stats = analyze_results(trades)
    display_report(stats)
