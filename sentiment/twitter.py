# sentiment/twitter.py

import requests

API_URL = "http://localhost:8001/twitter"

def fetch_twitter_sentiment(symbol: str):
    try:
        url = f"{API_URL}/{symbol}"
        response = requests.get(url, timeout=5)
        data = response.json()
        score = data.get("score", 0)
        return {"score": score}
    except Exception as e:
        print(f"⚠️ Twitter service error for {symbol}: {e}")
        return {"score": 0}
