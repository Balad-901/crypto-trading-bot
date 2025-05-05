# risk/trade_risk_manager.py

from risk.cooldown_manager import check_cooldown
from sentiment.multitimeframe import CURRENT_SENTIMENT
from sentiment.trend_detector import detect_sentiment_trend

def assess_trade_risk(symbol, confidence, volatility, timeframe):
    if check_cooldown():
        print("🚫 Risk Manager: Cooldown active. No trades allowed.")
        return False

    if confidence < 0.2:
        print("🚫 Risk Manager: Confidence too low. Skipping trade.")
        return False

    if volatility > 0.8:
        print("⚠️ Risk Manager: Volatility very high. Reduce position size.")
        # (Bot will automatically adjust position sizing elsewhere)

    sentiment_trend = detect_sentiment_trend()
    trend_for_tf = sentiment_trend.get(timeframe, "neutral")

    if trend_for_tf == "bearish" and symbol.endswith("USDT") and confidence > 0:
        print("⚠️ Risk Manager: Bearish trend detected, extra caution.")
    
    print("✅ Risk Manager: Trade allowed.")
    return True
