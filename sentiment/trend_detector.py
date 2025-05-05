from textblob import TextBlob

def detect_trend(sentences):
    if not sentences:
        return "neutral"
    
    total_sentiment = sum(TextBlob(sentence).sentiment.polarity for sentence in sentences) / len(sentences)
    
    if total_sentiment > 0.1:
        return "uptrend"
    elif total_sentiment < -0.1:
        return "downtrend"
    else:
        return "neutral"
