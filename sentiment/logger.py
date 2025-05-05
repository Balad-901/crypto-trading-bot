import json
import os
from datetime import datetime

LOG_FILE = "data/sentiment_log.json"

def save_sentiment_log(data):
    timestamp = datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "avg_sentiment": data.get("avg_sentiment", {}),
        "volatility": data.get("volatility", {})
    }

    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
