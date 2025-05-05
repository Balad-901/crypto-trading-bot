import json
from collections import defaultdict

LOG_FILE = "trades.json"

def analyze_trade_history():
    try:
        with open(LOG_FILE, "r") as f:
            trades = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No trades to analyze.")
        return {}

    summary = defaultdict(int)
    confidence_total = 0
    confidence_count = 0
    wins = 0
    losses = 0

    for trade in trades:
        decision = trade.get("decision")
        confidence = trade.get("confidence", 0)
        result = trade.get("result")

        summary[decision] += 1
        confidence_total += confidence
        confidence_count += 1

        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1

    average_confidence = (
        round(confidence_total / confidence_count, 3)
        if confidence_count > 0
        else 0
    )

    win_rate = (
        round(wins / (wins + losses), 3)
        if (wins + losses) > 0
        else None
    )

    learned_strategy = {
        "average_confidence": average_confidence,
        "total_trades": confidence_count,
        "decision_distribution": dict(summary),
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
    }

    print("📊 Learned Strategy Summary:")
    for k, v in learned_strategy.items():
        print(f"   {k}: {v}")

    return learned_strategy

if __name__ == "__main__":
    analyze_trade_history()
