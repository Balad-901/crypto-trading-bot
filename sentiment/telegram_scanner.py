# sentiment/telegram_scanner.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright
from llm.summary_agent import summarize_and_score
from utils.topic_classifier import classify_topic
from utils.influencer_detector import detect_influencers
from memory.writer import save_memory_summary

TELEGRAM_GROUPS = [
    "CryptoWhale",
    "CryptoBusy",
    "CryptoNews",
    "Bitcoin_Binance_Channel"
]

def scan_telegram(symbol: str):
    print(f"💬 Scanning Telegram for {symbol} mentions...")
    results = []

    token_name = symbol.replace("USDT", "").lower()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for group in TELEGRAM_GROUPS:
            url = f"https://t.me/s/{group}"
            try:
                page.goto(url, timeout=30000)
                page.wait_for_selector("div.tgme_widget_message_text", timeout=5000)
                posts = page.query_selector_all("div.tgme_widget_message_text")

                for post in posts[-30:]:
                    text = post.inner_text().strip()
                    if not text or len(text) < 40:
                        continue
                    if symbol.lower() not in text.lower() and token_name not in text.lower():
                        continue

                    results.append({
                        "group": group,
                        "text": text
                    })

            except Exception as e:
                print(f"❌ Failed to scan {group}: {e}")

        browser.close()

    # Process posts with GPT
    for post in results:
        text = post["text"]
        summary, sentiment, _ = summarize_and_score(text)
        topic = classify_topic(summary)
        influencers, influencer_boost = detect_influencers(text)

        print(f"💬 [TG:{post['group']}] {summary[:100]}... | Sentiment: {sentiment} | Topic: {topic}")

        save_memory_summary(
            symbol=symbol,
            summary=summary,
            sentiment=sentiment,
            topic=topic,
            extra={
                "influencers": influencers,
                "influencer_boost": influencer_boost,
                "source": f"https://t.me/s/{post['group']}"
            }
        )
