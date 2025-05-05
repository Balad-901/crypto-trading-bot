# research/runner.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser.scraper import search_web
from browser.youtube_scraper import scrape_youtube_videos
from sentiment.telegram_scanner import scan_telegram
from podcast.podcast_scanner import analyze_podcast

from llm.summary_agent import summarize_and_score
from llm.hype_detector import detect_hype
from memory.writer import save_memory_summary
from utils.sentiment_tracker import update_sentiment
from utils.influencer_detector import detect_influencers
from utils.topic_classifier import classify_topic

import json
from datetime import datetime

ALERT_KEYWORDS = ["panic", "fomo", "fear", "elon", "trump", "cz", "black swan", "dump", "moon"]
ALERT_LOG_PATH = "logs/alerts.jsonl"
os.makedirs("logs", exist_ok=True)

def log_alert(symbol, keyword, source, confidence, summary):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "keyword": keyword,
        "source": source,
        "confidence": confidence,
        "summary": summary
    }
    with open(ALERT_LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"⚠️ ALERT: {keyword.upper()} detected in {source} for {symbol} — confidence {confidence}")

def check_for_alerts(symbol, summary, confidence):
    text = summary.lower()
    for keyword in ALERT_KEYWORDS:
        if keyword in text:
            log_alert(symbol, keyword, "summary", confidence, summary)

def run_research(symbol: str):
    print(f"🔎 Running research for {symbol}...")

    # 🧠 Web scrape + LLM summary
    web_data = search_web(symbol)
    youtube_data = scrape_youtube_videos(symbol)
    telegram_data = scan_telegram(symbol)
    podcast_data = analyze_podcast(symbol)

    full_text = "\n".join([web_data, youtube_data, telegram_data, podcast_data])
    summary, confidence = summarize_and_score(full_text, symbol)

    check_for_alerts(symbol, summary, confidence)

    save_memory_summary(symbol, summary)
    update_sentiment(symbol, confidence)
    classify_topic(symbol, summary)
    detect_influencers(symbol, summary)
    detect_hype(symbol, summary)

    print(f"✅ Research complete for {symbol}")
