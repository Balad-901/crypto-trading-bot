# execution/binance.py

import os
import requests
import json
from utils.state import get_bot_status

# Your Binance Testnet API keys
BINANCE_API_KEY = "c75e1e33e4815517a57dc5b5662a3292041de7dbf5f6b0dbb9a05ea9aaa93346"
BINANCE_API_SECRET = "adf448fa9240357f09fdd778aa7dcc638a49312d0c8a98c8c91ceb7d5cc44469"

BASE_URL = "https://testnet.binancefuture.com"

HEADERS = {
    "X-MBX-APIKEY": BINANCE_API_KEY
}

def place_binance_order(symbol, side, quantity, test_mode=False):
    try:
        url = BASE_URL + "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side.upper(),  # BUY or SELL
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])

        # Sign request
        import hmac
        import hashlib
        signature = hmac.new(
            BINANCE_API_SECRET.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        params["signature"] = signature

        if test_mode:
            url += "/test"

        response = requests.post(url, headers=HEADERS, params=params)
        result = response.json()

        if response.status_code != 200:
            print(f"⚠️ Binance API error: {result}")
        else:
            print(f"✅ Order placed: {side} {quantity} {symbol}")

        return result

    except Exception as e:
        print(f"⚠️ Error placing Binance order: {e}")
        return None

def calculate_position_size(confidence, base_amount=20):
    """
    Smart Position Sizing:
    - If confidence is high → increase size
    - If low → decrease size
    """
    size = base_amount

    if confidence > 0.7:
        size *= 2  # double position
    elif confidence < 0.3:
        size *= 0.5  # reduce size

    return round(size, 3)

def should_hedge(sentiment_data):
    """
    Early Hedging Detector:
    - If volatility is very high + sentiment negative → possible hedge trigger
    """
    vol = sentiment_data.get("volatility", {})
    avg_volatility = (vol.get("twitter", 0) + vol.get("reddit", 0) + vol.get("news", 0)) / 3

    sentiment = sentiment_data.get("avg_sentiment", {})
    avg_sentiment = (sentiment.get("twitter", 0) + sentiment.get("reddit", 0) + sentiment.get("news", 0)) / 3

    return avg_volatility > 0.5 and avg_sentiment < -0.1
