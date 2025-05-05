# monitor/metrics.py

from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/dashboard/metrics")
def get_metrics():
    sentiment_data = {}
    heatmap_data = {}

    # Try loading sentiment data
    try:
        if os.path.exists("logs/sentiment/latest.json"):
            with open("logs/sentiment/latest.json", "r") as f:
                sentiment_data = json.load(f)
    except Exception as e:
        sentiment_data = {"error": str(e)}

    # Try loading heatmap data (later if needed)
    # Right now heatmap is skipped for simplicity

    return {
        "status": "success",
        "sentiment_trend": sentiment_data.get("avg_sentiment", {}),
        "heatmap": {}
    }
