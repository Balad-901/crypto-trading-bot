# stats_sources.py

import json
import os
from collections import defaultdict

DECISIONS_FILE = "logs/decisions.json"
RESULTS_FILE = "logs/results.json"

def load_decisions():
    if not os.path.exists(DECISIONS_FILE):
        print("⚠️ No decisions.json file found.")
        return []
    with open(DECISIONS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def load_results():
    if not os.path.exists(RESULTS_FILE):
        print("⚠️ No results.json file found.")
        return []
    with open(RESULTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def track_source_accuracy():
    decisions = load_decisions()
    results = load_results()

    source_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "total": 0})

    for i in range(min(len(decisions), len(results))):
        decision = decisions[i]
        result = results[i]
        outcome = result.get("result", "unknown")

        try:
            research = decision["result"]["details"]["research"]
            for source in ["reddit", "twitter", "news"]:
                score = research.get(source, {}).get("score", 0)
                if score != 0:
                    source_stats[source]["total"] += 1
                    if outcome == "win":
                        source_stats[source]["wins"] += 1
                    elif outcome == "loss":
                        source_stats[source]["losses"] += 1
        except Exception:
            continue

    return source_stats

def display_source_stats(source_stats):
    print("===================================")
    print(" 🧠 SIGNAL SOURCE ACCURACY REPORT")
    print("-----------------------------------")
    for source, stats in source_stats.items():
        total = stats["total"]
        win_rate = round((stats["wins"] / total) * 100, 2) if total else 0
        print(f" 🔹 {source.upper()}")
        print(f"     ✅ Wins     : {stats['wins']}")
        print(f"     ❌ Losses   : {stats['losses']}")
        print(f"     📊 Win Rate : {win_rate}%")
        print(f"     📦 Total    : {total}")
        print("-----------------------------------")
    print("===================================")

if __name__ == "__main__":
    stats = track_source_accuracy()
    display_source_stats(stats)
