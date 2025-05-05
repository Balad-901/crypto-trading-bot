# sentiment/alpha_feed.py

DYNAMIC_KEYWORDS = {
    "bullish": ["Bitcoin", "Ethereum", "bullish", "altcoins", "crypto rally"],
    "bearish": ["crypto crash", "recession", "bear market", "risk off", "FUD"],
    "neutral": ["blockchain", "crypto", "DeFi", "Web3", "NFT"]
}

CURRENT_KEYWORDS = DYNAMIC_KEYWORDS["neutral"]

def update_keywords(latest_sentiment):
    global CURRENT_KEYWORDS

    avg_sentiment = (latest_sentiment.get("twitter", 0) + 
                     latest_sentiment.get("reddit", 0) + 
                     latest_sentiment.get("news", 0)) / 3

    if avg_sentiment > 0.1:
        CURRENT_KEYWORDS = DYNAMIC_KEYWORDS["bullish"]
    elif avg_sentiment < -0.1:
        CURRENT_KEYWORDS = DYNAMIC_KEYWORDS["bearish"]
    else:
        CURRENT_KEYWORDS = DYNAMIC_KEYWORDS["neutral"]

    print(f"🔄 Alpha Feed adjusted: {CURRENT_KEYWORDS}")
    return CURRENT_KEYWORDS
