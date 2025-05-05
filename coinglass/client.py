import requests

COINGLASS_API_KEY = "0a79300218cc4454b6594f2b8a224781"
BASE_URL = "https://open-api.coinglass.com/public/v2"

HEADERS = {
    "accept": "application/json",
    "coinglassSecret": COINGLASS_API_KEY
}

def fetch_liquidation_data(symbol="BTCUSDT"):
    url = f"{BASE_URL}/liquidation_chart?symbol={symbol}&time_type=h1"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if data.get("code") == 0:
            return data.get("data", {})
        else:
            print("❌ Coinglass error:", data.get("msg"))
            return {}
    except Exception as e:
        print("⚠️ Coinglass fetch error:", str(e))
        return {}

def get_liquidation_summary(symbol="BTCUSDT"):
    data = fetch_liquidation_data(symbol)
    long_total = sum(x.get("longVolUsd", 0) for x in data.get("list", []))
    short_total = sum(x.get("shortVolUsd", 0) for x in data.get("list", []))

    if long_total + short_total == 0:
        return {"bias": "neutral", "long": 0, "short": 0}

    bias = "bullish" if long_total > short_total else "bearish" if short_total > long_total else "neutral"

    return {
        "bias": bias,
        "long": long_total,
        "short": short_total
    }
