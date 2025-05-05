# technical/signals.py

import requests
import pandas as pd

BINANCE_API = "https://api.binance.com/api/v3/klines"

def get_price_data(symbol="BTCUSDT", interval="1h", limit=200):
    try:
        url = f"{BINANCE_API}?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url, timeout=10)
        raw = response.json()

        df = pd.DataFrame(raw, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])
        df["volume"] = pd.to_numeric(df["volume"])
        return df[["timestamp", "close", "volume"]]
    except Exception as e:
        print(f"⚠️ Error fetching Binance price data: {e}")
        return None

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def get_trend(prices):
    return 1 if prices.iloc[-1] > prices.iloc[-10] else -1

def calculate_moving_averages(prices):
    ma50 = prices.rolling(50).mean().iloc[-1]
    ma200 = prices.rolling(200).mean().iloc[-1]
    return ma50, ma200

def get_technical_signal(symbol="BTCUSDT", timeframe="1h"):
    df = get_price_data(symbol, interval=timeframe)
    if df is None or len(df) < 200:
        return {
            "rsi": 50,
            "trend": 0,
            "ma_signal": 0
        }

    rsi = round(calculate_rsi(df["close"]), 2)
    trend = get_trend(df["close"])
    ma50, ma200 = calculate_moving_averages(df["close"])

    ma_signal = 1 if ma50 > ma200 else -1

    return {
        "rsi": rsi,
        "trend": trend,
        "ma_signal": ma_signal
    }
