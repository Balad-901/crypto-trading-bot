# twitter_sentiment_service.py

from fastapi import FastAPI
from sentiment.twitter import fetch_twitter_sentiment
import uvicorn

app = FastAPI()

@app.get("/twitter/{symbol}")
def get_sentiment(symbol: str):
    try:
        sentiment = fetch_twitter_sentiment(symbol)
        return {"symbol": symbol, "score": sentiment.get("score", 0)}
    except Exception as e:
        return {"symbol": symbol, "score": 0, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
