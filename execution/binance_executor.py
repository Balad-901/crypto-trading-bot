# execution/binance_executor.py

import requests
import time
import hmac
import hashlib
import logging
from urllib.parse import urlencode
from datetime import datetime
from logger import log_event

# ✅ Insert your actual API keys here
BINANCE_API_KEY = "YZYi3t2kxIZG2rZIHN0fcsYdq"
BINANCE_API_SECRET = "QhNcaTh9n2sfyWGiukL9j5RTi6lgLZEVa2FeZMMfXbwK33fXDf"
BINANCE_BASE_URL = "https://testnet.binance.vision"  # Use "https://api.binance.com" for live

def get_headers():
    return {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

def get_server_time():
    url = f"{BINANCE_BASE_URL}/api/v3/time"
    response = requests.get(url)
    return response.json()["serverTime"]

def sign_params(params):
    query = urlencode(params)
    signature = hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return f"{query}&signature={signature}"

def place_order(symbol, side, quantity):
    try:
        url = f"{BINANCE_BASE_URL}/api/v3/order"

        params = {
            "symbol": symbol,
            "side": side.upper(),        # BUY or SELL
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": get_server_time()
        }

        signed_params = sign_params(params)
        response = requests.post(url, headers=get_headers(), params=signed_params)
        response.raise_for_status()
        result = response.json()

        log_event("live_orders.json", {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "status": "submitted",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

        print(f"✅ [BINANCE] Order placed: {side} {quantity} {symbol}")
        return result

    except Exception as e:
        logging.error(f"[BINANCE ERROR] {e}")
        return {"error": str(e)}
