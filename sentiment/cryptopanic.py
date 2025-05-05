import requests

def fetch_cryptopanic_sentiment(api_key):
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&filter=important"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        headlines = [post["title"] for post in data.get("results", [])]
        positive_keywords = ["bullish", "pump", "rally", "surge", "breakout"]
        negative_keywords = ["bearish", "dump", "crash", "retrace", "collapse"]

        score = 0
        for headline in headlines:
            lowered = headline.lower()
            if any(word in lowered for word in positive_keywords):
                score += 1
            if any(word in lowered for word in negative_keywords):
                score -= 1

        return score
    except Exception as e:
        print(f"❌ Error fetching CryptoPanic sentiment: {e}")
        return 0
