# binance/binance.py

import os
import requests

API_KEY = "c75e1e33e4815517a57dc5b5662a3292041de7dbf5f6b0dbb9a05ea9aaa93346"
API_SECRET = "adf448fa9240357f09fdd778aa7dcc638a49312d0c8a98c8c91ceb7d5cc44469"
BASE_URL = "https://testnet.binancefuture.com"

def place_test_order(symbol, side, quantity):
    url = f"{BASE_URL}/fapi/v1/order/test"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(requests.get(f"{BASE_URL}/fapi/v1/time").json()["serverTime"])
    }
    try:
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            return {"status": "success", "details": response.json()}
        else:
            return {"status": "error", "details": response.text}
    except Exception as e:
        return {"status": "error", "details": str(e)}
