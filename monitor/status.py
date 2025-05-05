# monitor/status.py

import json
import os

def get_full_status():
    try:
        with open("logs/sentiment/latest.json", "r") as f:
            sentiment_data = json.load(f)
    except Exception as e:
        sentiment_data = {"error": str(e)}

    heatmap_data = {}  # (Optionally you can later improve heatmap pulling here)

    return {
        "status": "success",
        "sentiment_trend": sentiment_data.get("avg_sentiment", {}),
        "heatmap": heatmap_data
    }
