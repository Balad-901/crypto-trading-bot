# coinglass/coinglass.py

import os
import requests
import time

COINGLASS_API_KEY = "c75e1e33e4815517a57dc5b5662a3292041de7dbf5f6b0dbb9a05ea9aaa93346"

def get_liquidation_heatmap(symbol="BTCUSDT", retries=3, delay=5):
    url = f"https://open-api.coinglass.com/public/v2/liquidation_map?symbol={symbol}"
    headers = {
        "accept": "application/json",
        "coinglassSecret": COINGLASS_API_KEY
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Warning: Coinglass error {response.status_code}. Retrying...")
                time.sleep(delay)
        except Exception as e:
            print(f"Error contacting Coinglass: {e}. Retrying...")
            time.sleep(delay)
    return {"error": "Coinglass unavailable after retries"}
