# memory/replayer.py

import json
import os
from collections import defaultdict

def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return fallback

def replay_memory():
    decisions_path = os.path.join("memory", "decisions.json")
    trades_path = os.path.join("memory", "trades.json")

    decisions = load_json(decisions_path, [])
    trades = load_json(trades_path, [])

    topic_stats = defaultdict(lambda: {"count": 0, "total_pnl": 0.0})
    influencer_stats = defaultdict(lambda: {"count": 0, "total_pnl": 0.0})

    for decision in decisions:
        symbol = decision.get("symbol")
        topic = decision.get("topic")
        influencers = decision.get("influencers", [])

        matching_trade = next((t for t in trades if t.get("symbol") == symbol and abs(t.get("confidence", 0) - decision.get("confidence", 0)) < 0.01), None)

        if matching_trade:
            pnl = matching_trade.get("pnl", 0.0)
            if topic:
                topic_stats[topic]["count"] += 1
                topic_stats[topic]["total_pnl"] += pnl
            for inf in influencers:
                influencer_stats[inf]["count"] += 1
                influencer_stats[inf]["total_pnl"] += pnl

    print("\n📈 Topic Replay Summary:")
    for topic, stats in topic_stats.items():
        avg = stats["total_pnl"] / stats["count"] if stats["count"] > 0 else 0
        print(f"🔹 {topic}: {stats['count']} trades | Avg PnL: {avg:.2f}%")

    print("\n👤 Influencer Replay Summary:")
    for inf, stats in influencer_stats.items():
        avg = stats["total_pnl"] / stats["count"] if stats["count"] > 0 else 0
        print(f"🔹 {inf}: {stats['count']} trades | Avg PnL: {avg:.2f}%")

if __name__ == "__main__":
    replay_memory()
