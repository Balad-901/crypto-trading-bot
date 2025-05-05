# decision/engine.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.sentiment_tracker import get_sentiment
from decision.confidence_engine import get_confidence_boost
from execution.trader import simulate_trade

def calculate_confidence(symbol: str, topic: str, influencers: list) -> float:
    base = get_sentiment(symbol)
    boost = get_confidence_boost(topic, influencers)

    total = base + boost
    print(f"🤖 Final Confidence for {symbol}: {total:.2f} (base: {base:.2f} + memory: {boost:.2f})")
    return total

def should_trade(symbol: str, topic: str, influencers: list, threshold=0.5) -> bool:
    confidence = calculate_confidence(symbol, topic, influencers)
    return confidence >= threshold

def make_decision(symbol: str, topic: str, influencers: list) -> dict:
    confidence = calculate_confidence(symbol, topic, influencers)
    action = "buy" if confidence >= 0.5 else "hold"

    decision = {
        "symbol": symbol,
        "topic": topic,
        "influencers": influencers,
        "confidence": confidence,
        "action": action
    }

    # Trigger simulated trade with SL/TP logic
    if action == "buy":
        simulate_trade(symbol, confidence)

    return decision
