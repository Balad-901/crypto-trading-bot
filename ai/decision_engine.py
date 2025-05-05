from sentiment.summary import get_sentiment_summary

def make_trade_decision(symbol: str, signal: str, timeframe: str):
    sentiment = get_sentiment_summary()

    avg_sentiment = (
        sentiment["avg_sentiment"]["twitter"]
        + sentiment["avg_sentiment"]["reddit"]
        + sentiment["avg_sentiment"]["news"]
    ) / 3

    volatility = (
        sentiment["volatility"]["twitter"]
        + sentiment["volatility"]["reddit"]
        + sentiment["volatility"]["news"]
    ) / 3

    confidence = avg_sentiment - volatility

    if confidence > 0.1:
        decision = signal
        reason = "✅ Confidence high, executing signal"
    elif confidence < -0.1:
        decision = "hold"
        reason = "⚠️ Confidence low, holding position"
    else:
        decision = "hold"
        reason = "Neutral signal, waiting for better opportunity"

    return {
        "symbol": symbol,
        "signal": signal,
        "timeframe": timeframe,
        "avg_sentiment": round(avg_sentiment, 3),
        "volatility": round(volatility, 3),
        "confidence": round(confidence, 3),
        "decision": decision,
        "reason": reason
    }
