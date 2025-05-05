import httpx

BASE_URL = "https://api.binance.com/api/v3"

def get_current_price(symbol="BTCUSDT"):
    try:
        res = httpx.get(f"{BASE_URL}/ticker/price", params={"symbol": symbol}, timeout=10)
        data = res.json()
        return float(data.get("price", 0))
    except Exception as e:
        print(f"❌ Price error: {e}")
        return 0.0
