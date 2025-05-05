# sentiment/cryptopanic.py

import requests
import logging

# ✅ Your actual CryptoPanic API key
CRYPTO_PANIC_KEY = "3aa67cc0b926f51c8405da5616d339d2b69ac981"

def fetch_cryptopanic_sentiment(symbol: str):
    try:
        url = (
            f"https://cryptopanic.com/api/v1/posts/"
            f"?auth_token={CRYPTO_PANIC_KEY}&currencies={symbol.lower()}&filter=hot"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("results", [])

        score = sum(1 for d in data if d.get("positive")) - sum(1 for d in data if d.get("negative"))

        return {"score": score, "count": len(data)}

    except Exception as e:
        logging.error(f"[NEWS] Error: {e}")
        return {"score": 0, "count": 0}
