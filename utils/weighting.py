# utils/weighting.py

from utils.pnl_tracker import load_trades

def score_sources(symbol):
    """
    Analyze past trades and determine which sources (Twitter, News, Memory)
    were most predictive of profitable outcomes.
    Returns a weight dict.
    """
    trades = load_trades()
    symbol_trades = [t for t in trades if t["symbol"] == symbol and "scores" in t]

    # Initialize source scores
    source_totals = {"twitter": 0, "news": 0, "memory": 0}
    source_counts = {"twitter": 0.001, "news": 0.001, "memory": 0.001}  # prevent division by zero

    for t in symbol_trades:
        pnl = t["pnl"]
        for source in ["twitter", "news", "memory"]:
            score = t["scores"].get(source, 0)
            source_totals[source] += score * pnl
            source_counts[source] += abs(score)

    # Calculate weighted average impact
    weights = {}
    for source in source_totals:
        weights[source] = round(source_totals[source] / source_counts[source], 3)

    # Normalize weights (so they sum to ~1)
    total_weight = sum(abs(w) for w in weights.values()) or 1
    for source in weights:
        weights[source] = round(weights[source] / total_weight, 3)

    return weights
