# utils/topic_classifier.py

TOPIC_KEYWORDS = {
    "ETF": ["etf", "blackrock", "spot etf", "securities filing", "bitcoin etf"],
    "Regulation": ["sec", "regulation", "law", "lawsuit", "court", "ban", "approval", "rejected"],
    "Hack": ["hack", "exploit", "drained", "breach", "attack", "compromised"],
    "Adoption": ["partnership", "collaboration", "adoption", "integration", "expansion", "launched"],
    "Macro": ["interest rate", "cpi", "inflation", "macro", "fed", "federal reserve"],
    "FUD": ["fear", "uncertainty", "doubt", "collapse", "crash", "panic"],
    "Bullish": ["bullish", "surge", "pump", "rally", "breakout", "parabolic"],
    "Bearish": ["bearish", "dump", "crash", "plunge", "sell-off", "capitulation"]
}

def classify_topic(text: str):
    detected = set()
    text = text.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for word in keywords:
            if word in text:
                detected.add(topic)
                break  # Only need 1 match per topic

    return ", ".join(sorted(detected)) if detected else "Unknown"
