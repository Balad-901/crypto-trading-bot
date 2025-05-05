# sentiment/vpn_twitter_fetcher.py

import requests
import sys
import json
import logging

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH4p0wEAAAAATvhyTuPW1XcSK76yX%2FTI5ejkxOE%3DizcAaXSI3PAXOfBcZ7g9C0gttwutcFtP8qFJrjOukTk4kn6jMf"

def fetch_sentiment(symbol: str):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }

    query = f"{symbol} crypto -is:retweet lang:en"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=20"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        tweets = response.json().get("data", [])
        score = sum(1 for t in tweets if "bullish" in t["text"].lower()) - sum(
            1 for t in tweets if "bearish" in t["text"].lower()
        )
        print(json.dumps({"score": score, "count": len(tweets)}))
    except Exception as e:
        logging.error(f"[VPN FETCHER] Twitter error: {e}")
        print(json.dumps({"score": 0, "count": 0}))

if __name__ == "__main__":
    symbol = sys.argv[1]
    fetch_sentiment(symbol)

