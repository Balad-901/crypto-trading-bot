# update_weights.py

import json
import os

DECISIONS_FILE = "logs/decisions.json"
RESULTS_FILE = "logs/results.json"
WEIGHTS_FILE = "logs/source_weights.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_weights(weights):
    with open(WEIGHTS_FILE, "w") as f:
        json.dump(weights, f, indent=2)

def update_weights():
    decisions = load_json(DECISIONS_FILE)
    results = load_json(RESULTS_FILE)

    total = {"twitter": 0, "reddit": 0, "news": 0}
    wins = {"twitter": 0, "reddit": 0, "news": 0}

    for i in range(min(len(decisions), len(results))):
        res = results[i]
        dec = decisions[i]
        outcome = res.get("result")
        research = dec.get("data", {}).get("result", {}).get("details", {}).get("research", {})
        for src in ["twitter", "reddit", "news"]:
            if research.get(src, {}).get("score", 0) != 0:
                total[src] += 1
                if outcome == "win":
                    wins[src] += 1

    weights = {}
    for src in total:
        if total[src] > 0:
            weights[src] = round(1 + ((wins[src] / total[src]) - 0.5), 2)
        else:
            weights[src] = 1.0

    save_weights(weights)
    print("✅ Updated weights:", weights)

if __name__ == "__main__":
    update_weights()
