# sentiment/research_engine.py

import json
import os
from sentiment.twitter import fetch_twitter_sentiment
from sentiment.reddit import fetch_reddit_sentiment
from sentiment.cryptopanic import fetch_crypto_sentiment

SOURCE_WEIGHTS_FILE = "logs/source_weights.json"

def get_source_weights():
    if not os.path.exists(SOURCE_WEIGHTS_FILE):
        return {"twitter": 1.0, "reddit": 1.0, "news": 1.0}
    with open(SOURCE_WEIGHTS_FILE, "r") as f:
        return json.load(f)

def run_research(symbol="BTCUSDT"):
    twitter = fetch_twitter_sentiment(symbol)
    reddit = fetch_reddit_sentiment(symbol)
    news = fetch_crypto_sentiment(symbol)

    weights = get_source_weights()

    weighted_score = (
        weights.get("twitter", 1.0) * twitter["score"] +
        weights.get("reddit", 1.0) * reddit["score"] +
        weights.get("news", 1.0) * news["score"]
    )

    summary_score = round(weighted_score, 2)

    return {
        "symbol": symbol,
        "twitter": twitter,
        "reddit": reddit,
        "news": news,
        "weights": weights,
        "summary_score": summary_score
    }
