# utils/influencer_detector.py

INFLUENCERS = {
    "elon musk": 0.3,
    "cz": 0.25,
    "changpeng zhao": 0.25,
    "donald trump": 0.2,
    "michael saylor": 0.2,
    "vitalik buterin": 0.15,
    "gary gensler": -0.2,
    "sec chair": -0.2,
    "sam bankman-fried": -0.5,
    "sbf": -0.5
}

def detect_influencers(text: str):
    """
    Returns a list of matched influencers and their combined confidence boost/penalty.
    """
    text_lower = text.lower()
    found = []
    total_weight = 0.0

    for name, weight in INFLUENCERS.items():
        if name in text_lower:
            found.append(name)
            total_weight += weight

    return {
        "influencers": found,
        "influencer_boost": round(total_weight, 3)
    }
