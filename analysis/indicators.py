# analysis/indicators.py

import pandas as pd
import ta

def calculate_indicators(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 50:
        return {}

    # Make sure 'close' is float
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    indicators = {}

    # RSI (14)
    rsi = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
    indicators["rsi"] = rsi.iloc[-1]

    # MACD
    macd = ta.trend.MACD(close=df["close"])
    indicators["macd"] = macd.macd().iloc[-1]
    indicators["macd_signal"] = macd.macd_signal().iloc[-1]

    # EMA 20
    ema20 = ta.trend.EMAIndicator(close=df["close"], window=20).ema_indicator()
    indicators["ema20"] = ema20.iloc[-1]

    # Bollinger Bands (20, 2)
    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    indicators["bb_upper"] = bb.bollinger_hband().iloc[-1]
    indicators["bb_lower"] = bb.bollinger_lband().iloc[-1]

    return indicators
