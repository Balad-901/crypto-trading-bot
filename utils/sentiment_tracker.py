# utils/sentiment_tracker.py

sentiment_scores = {}

def update_sentiment(symbol: str, score: float):
    """Update the latest sentiment score for a given symbol."""
    sentiment_scores[symbol] = score

def get_sentiment(symbol: str) -> float:
    """Get the latest sentiment score for a given symbol."""
    return sentiment_scores.get(symbol, 0)
