# sentiment/multitimeframe.py

SENTIMENT_MEMORY = {
    "24h": [],
    "7d": []
}

def get_multi_timeframe_sentiment(symbol):
    # Simple average calculation (can upgrade later)
    last_24h = SENTIMENT_MEMORY.get("24h", [])
    last_7d = SENTIMENT_MEMORY.get("7d", [])

    avg_24h = sum(last_24h) / len(last_24h) if last_24h else 0
    avg_7d = sum(last_7d) / len(last_7d) if last_7d else 0

    # Simple logic: trending if avg improving
    trend_score = avg_24h - avg_7d

    return {"trend_score": trend_score}
