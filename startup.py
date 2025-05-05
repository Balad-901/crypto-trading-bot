# startup.py

import json
import os

MEMORY_DIR = "memory"
LOG_DIR = "logs"

memory = {
    "decisions": [],
    "biases": {},
    "bias_log": [],
    "sentiment_history": {}
}

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def load_jsonl(path):
    if not os.path.exists(path):
        return []
    lines = []
    with open(path, "r") as f:
        for line in f:
            try:
                lines.append(json.loads(line.strip()))
            except:
                continue
    return lines

def load_memory():
    memory["decisions"] = load_json(os.path.join(MEMORY_DIR, "decisions.json"), [])
    memory["biases"] = load_json(os.path.join(MEMORY_DIR, "biases.json"), {})
    memory["sentiment_history"] = load_json(os.path.join(MEMORY_DIR, "sentiment_history.json"), {})
    memory["bias_log"] = load_jsonl(os.path.join(LOG_DIR, "biases_log.jsonl"))

    print("✅ Memory loaded:")
    print(f"• Decisions: {len(memory['decisions'])}")
    print(f"• Biases: {len(memory['biases'])}")
    print(f"• Sentiment days: {len(memory['sentiment_history'])}")
    print(f"• Bias log entries: {len(memory['bias_log'])}")

    return memory
