# execution/pnl_tracker.py

import requests
import logging

def get_current_price(symbol: str):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return round(float(response.json()["price"]), 2)
    except Exception as e:
        logging.error(f"[PNL] Price fetch error: {e}")
        return None

def calculate_pnl(entry_price: float, position_size: float, symbol: str):
    current_price = get_current_price(symbol)
    if current_price is None:
        return {"pnl": 0.0, "percent": 0.0}

    price_diff = current_price - entry_price
    pnl = round(price_diff * (position_size / entry_price), 2)
    percent = round((price_diff / entry_price) * 100, 2)

    return {"pnl": pnl, "percent": percent, "current_price": current_price}
