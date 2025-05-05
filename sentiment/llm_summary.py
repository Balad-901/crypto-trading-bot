# sentiment/llm_summary.py

def generate_market_summary(research: dict) -> str:
    twitter_score = research["twitter"]["score"]
    reddit_score = research["reddit"]["score"]
    news_score = research["news"]["score"]

    total_sources = 3
    combined_score = twitter_score + reddit_score + news_score

    if combined_score == 0:
        return "Market sentiment is neutral. No strong bias from any source."

    summary = []

    # Twitter
    if twitter_score > 0:
        summary.append("Twitter shows bullish chatter.")
    elif twitter_score < 0:
        summary.append("Twitter sentiment is bearish.")
    else:
        summary.append("Twitter is quiet.")

    # Reddit
    if reddit_score > 0:
        summary.append("Reddit is showing optimism.")
    elif reddit_score < 0:
        summary.append("Reddit shows bearish community signals.")
    else:
        summary.append("No clear direction from Reddit.")

    # News
    if news_score > 0:
        summary.append("News sentiment is positive.")
    elif news_score < 0:
        summary.append("News is showing negative headlines.")
    else:
        summary.append("No major news momentum.")

    summary.append(f"Combined sentiment score: {combined_score} across {total_sources} sources.")
    return " ".join(summary)
