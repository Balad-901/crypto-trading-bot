import json
from datetime import datetime, timedelta

def load_memory(filepath="memory/research_memory.json"):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_recent_sentiment(symbol, hours=12):
    memory = load_memory()
    recent_time = datetime.utcnow() - timedelta(hours=hours)
    scores = []

    for item in memory:
        if item.get("symbol") == symbol.upper():
            timestamp = item.get("timestamp")
            if timestamp:
                try:
                    item_time = datetime.fromisoformat(timestamp)
                    if item_time >= recent_time:
                        sentiment = item.get("sentiment_score")
                        if sentiment is not None:
                            scores.append(sentiment)
                except Exception:
                    continue

    if not scores:
        return None

    average_sentiment = sum(scores) / len(scores)
    return average_sentiment
