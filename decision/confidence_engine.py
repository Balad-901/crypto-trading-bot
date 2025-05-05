# decision/confidence_engine.py

import os
import json

BIAS_PATH = "memory/biases.json"

# Default in case no bias file exists
DEFAULT_BIAS = {
    "etf": 0.2,
    "regulation": -0.1,
    "whale": 0.15,
    "binance": 0.1,
    "elon": 0.2,
    "cz": 0.15,
    "fomo": -0.2,
    "panic": -0.25,
    "bullish": 0.15,
    "bearish": -0.05,
    "volume": 0.15,
    "moving average": 0.1
}

def load_biases():
    if not os.path.exists(BIAS_PATH):
        return DEFAULT_BIAS
    try:
        with open(BIAS_PATH, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_BIAS

def get_confidence_boost(topic: str, influencers: list) -> float:
    topic = topic.lower()
    bias_map = load_biases()
    boost = 0.0

    # Topic weight from bias map
    for keyword, weight in bias_map.items():
        if keyword in topic:
            boost += weight

    # Influencer effects
    for inf in influencers:
        inf_lower = inf.lower()
        if "elon" in inf_lower:
            boost += 0.2
        if "cz" in inf_lower:
            boost += 0.15
        if "gensler" in inf_lower:
            boost -= 0.2

    return round(boost, 3)
