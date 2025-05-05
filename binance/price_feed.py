import requests

BINANCE_BASE_URL = "https://testnet.binancefuture.com"

def get_current_price(symbol):
    url = f"{BINANCE_BASE_URL}/fapi/v1/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"Error fetching Binance price: {e}")
        return None
