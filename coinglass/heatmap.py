# coinglass/heatmap.py

import requests

COINGLASS_API_KEY = "your_real_coinglass_api_key"

def get_liquidation_heatmap(symbol="BTCUSDT"):
    url = f"https://open-api.coinglass.com/public/v2/liquidation_map?symbol={symbol}"
    headers = {
        "accept": "application/json",
        "coinglassSecret": COINGLASS_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            return {"error": "Rate limit hit from Coinglass (429)"}
        elif response.status_code == 500:
            return {"error": "Server error from Coinglass (500)"}
        else:
            return {"error": f"Unexpected error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
