# memory/reader.py

import json
import os

LOG_PATH = "logs/sentiment_history.json"

def fetch_memory_sentiment(symbol: str):
    if not os.path.exists(LOG_PATH):
        return 0.0

    with open(LOG_PATH, "r") as f:
        memory = json.load(f)

    entries = memory.get(symbol, [])
    if not entries:
        return 0.0

    sentiments = [e.get("sentiment", 0) for e in entries]
    avg = sum(sentiments) / len(sentiments)
    return round(avg, 3)

def fetch_memory_topic(symbol: str):
    if not os.path.exists(LOG_PATH):
        return ""

    with open(LOG_PATH, "r") as f:
        memory = json.load(f)

    entries = memory.get(symbol, [])
    topics = [e.get("topic", "") for e in entries]
    return ", ".join(topics[-3:])  # Return last 3 topics

def fetch_memory_influencers(symbol: str):
    if not os.path.exists(LOG_PATH):
        return {"influencers": [], "influencer_boost": 0.0}

    with open(LOG_PATH, "r") as f:
        memory = json.load(f)

    entries = memory.get(symbol, [])
    all_names = []
    total_boost = 0.0

    for e in entries[-5:]:
        if "influencers" in e:
            all_names += e["influencers"]
        if "influencer_boost" in e:
            total_boost += e["influencer_boost"]

    return {
        "influencers": list(set(all_names)),
        "influencer_boost": round(total_boost / max(len(entries[-5:]), 1), 3)
    }
