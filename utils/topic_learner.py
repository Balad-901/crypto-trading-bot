# utils/topic_learner.py

import json
import os
from collections import defaultdict

TRADE_LOG = "logs/trades.json"

def load_trades():
    if not os.path.exists(TRADE_LOG):
        return []
    with open(TRADE_LOG, "r") as f:
        return json.load(f)

def topic_avg_pnl():
    trades = load_trades()
    topic_pnl = defaultdict(float)
    topic_counts = defaultdict(int)

    for t in trades:
        pnl = t.get("pnl", 0)
        topic = t.get("topic", "Unknown")
        if not topic:
            continue

        # Handle multiple comma-separated topics (e.g., "FUD, Hack")
        for subtopic in topic.split(","):
            key = subtopic.strip()
            topic_pnl[key] += pnl
            topic_counts[key] += 1

    topic_averages = {}
    for topic, total in topic_pnl.items():
        count = topic_counts[topic]
        topic_averages[topic] = round(total / count, 4) if count else 0.0

    return topic_averages
