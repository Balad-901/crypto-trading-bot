# research/cryptopanic_scanner.py

import requests
import re
from summary.llm_summary import clean_text

CRYPTO_PANIC_API_KEY = "3aa67cc0b926f51c8405da5616d339d2b69ac981"

HOT_KEYWORDS = [
    "ETF", "hack", "rug", "lawsuit", "SEC", "investigation",
    "bullish", "bearish", "whale", "FUD", "pump", "dump"
]

def fetch_and_scan_news(symbol="BTC"):
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_API_KEY}&currencies={symbol}&public=true"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"score": 0, "keywords": [], "raw": "", "error": response.text}

        articles = response.json().get("results", [])
        titles = " ".join([a.get("title", "") for a in articles])
        text = clean_text(titles)

        matched_keywords = [kw for kw in HOT_KEYWORDS if re.search(rf"\b{kw}\b", text, re.IGNORECASE)]
        score = len(matched_keywords) * 10  # 10 pts per keyword hit

        return {
            "score": min(score, 100),
            "keywords": matched_keywords,
            "raw": text
        }

    except Exception as e:
        return {"score": 0, "keywords": [], "error": str(e), "raw": ""}
