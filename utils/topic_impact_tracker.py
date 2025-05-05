# utils/topic_impact_tracker.py

import json
import os

DECISIONS_FILE = "logs/decisions.json"

def compute_topic_profitability():
    if not os.path.exists(DECISIONS_FILE):
        return {}

    with open(DECISIONS_FILE, "r") as f:
        decisions = json.load(f)

    topic_pnls = {}
    topic_counts = {}

    for entry in decisions:
        topic = entry.get("topic", "")
        pnl = entry.get("simulated_pnl", 0)

        for t in topic.split(","):
            t = t.strip()
            if not t:
                continue

            topic_pnls[t] = topic_pnls.get(t, 0) + pnl
            topic_counts[t] = topic_counts.get(t, 0) + 1

    # Calculate average PnL per topic
    result = {}
    for topic, total_pnl in topic_pnls.items():
        count = topic_counts.get(topic, 1)
        result[topic] = round(total_pnl / count, 4)

    return result
