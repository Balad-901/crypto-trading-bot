import requests
import os

COINGLASS_API_KEY = os.getenv("COINGLASS_API_KEY", "your_real_api_key_here")

def get_liquidation_heatmap(symbol="BTCUSDT"):
    url = f"https://open-api.coinglass.com/public/v2/liquidation_map?symbol={symbol}"
    headers = {
        "accept": "application/json",
        "coinglassSecret": COINGLASS_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {})
        else:
            print(f"Coinglass API error: {response.status_code} {response.text}")
            return {}
    except Exception as e:
        print(f"Failed to fetch liquidation heatmap: {str(e)}")
        return {}
