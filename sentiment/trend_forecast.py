# sentiment/trend_forecast.py

def forecast_trend(research: dict) -> str:
    twitter_score = research["twitter"]["score"]
    reddit_score = research["reddit"]["score"]
    news_score = research["news"]["score"]
    total = twitter_score + reddit_score + news_score

    # Heuristic logic like a veteran trader
    if total >= 4:
        return "Strong bullish sentiment across sources. Uptrend likely to continue."
    elif total >= 2:
        return "Moderate bullish sentiment detected. Trend leaning upward."
    elif total == 1:
        return "Slightly bullish sentiment. Trend is unstable or forming."
    elif total == 0:
        return "Neutral sentiment. No clear trend direction yet."
    elif total == -1:
        return "Slightly bearish sentiment. Trend is weak or shifting."
    elif total <= -2:
        return "Consistent bearish sentiment. Trend is likely downward."
    else:
        return "Strong bearish signals. Expect continued downtrend."
