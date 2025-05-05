import requests
import json
import os
from datetime import datetime, timedelta
from textblob import TextBlob

TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAH4p0wEAAAAAHeTvlQ07ECHTIa5iF9kwCAJCxD8%3DdFqfuH0t8ckBFWDb9s3u4y21ldC22AfBxA3lkh0wYPeBkJ617y"
REDDIT_API_KEY = "eItonquMZVRvMIu9HfncUJun0ka2hA"
CRYPTOPANIC_API_KEY = "3aa67cc0b926f51c8405da5616d339d2b69ac981"

def fetch_twitter_sentiment():
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    queries = ["Bitcoin", "Crypto", "Ethereum", "Altcoins", "Blockchain"]
    sentiments = []

    for query in queries:
        try:
            url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=text"
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                for tweet in data.get("data", []):
                    text = tweet["text"]
                    score = TextBlob(text).sentiment.polarity
                    sentiments.append(score)
            else:
                sentiments.append(0)
        except Exception:
            sentiments.append(0)

    return sentiments

def fetch_reddit_sentiment():
    try:
        url = f"https://api.pushshift.io/reddit/search/submission/?q=crypto&sort=desc&size=10"
        resp = requests.get(url)
        sentiments = []
        if resp.status_code == 200:
            data = resp.json()
            for post in data.get("data", []):
                text = post.get("title", "")
                score = TextBlob(text).sentiment.polarity
                sentiments.append(score)
        return sentiments
    except Exception:
        return [0]

def fetch_news_sentiment():
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&public=true&filter=news"
        resp = requests.get(url)
        sentiments = []
        if resp.status_code == 200:
            data = resp.json()
            for article in data.get("results", []):
                title = article.get("title", "")
                score = TextBlob(title).sentiment.polarity
                sentiments.append(score)
        return sentiments
    except Exception:
        return [0]

def calculate_average(sentiments):
    if sentiments:
        return sum(sentiments) / len(sentiments)
    return 0

def save_sentiment_log(current_data):
    now = datetime.utcnow()
    logs_folder = "sentiment_logs"
    os.makedirs(logs_folder, exist_ok=True)
    filename = os.path.join(logs_folder, f"log_{now.strftime('%Y%m%d')}.json")

    log = {
        "timestamp": now.isoformat(),
        "data": current_data
    }

    with open(filename, "w") as f:
        json.dump(log, f)

def load_previous_sentiment(days_ago=1):
    target_date = datetime.utcnow() - timedelta(days=days_ago)
    filename = f"sentiment_logs/log_{target_date.strftime('%Y%m%d')}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            log = json.load(f)
            return log["data"]
    return None

def get_sentiment_summary():
    twitter_sentiments = fetch_twitter_sentiment()
    reddit_sentiments = fetch_reddit_sentiment()
    news_sentiments = fetch_news_sentiment()

    current_sentiment = {
        "twitter": calculate_average(twitter_sentiments),
        "reddit": calculate_average(reddit_sentiments),
        "news": calculate_average(news_sentiments),
    }

    previous_sentiment = load_previous_sentiment()

    delta = {}
    if previous_sentiment:
        for key in current_sentiment:
            delta[key] = current_sentiment[key] - previous_sentiment.get(key, 0)
    else:
        delta = {"twitter": 0, "reddit": 0, "news": 0}

    result = {
        "current_sentiment": current_sentiment,
        "delta_24h": delta
    }

    save_sentiment_log(current_sentiment)

    return result
