# llm/summary_agent.py

import openai
import os
import json
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

TRUST_PATH = "memory/trust_weights.json"
DEFAULT_SOURCE_TRUST = 0.6
DEFAULT_TOPIC_TRUST = 1.0

def load_trust_config():
    if os.path.exists(TRUST_PATH):
        with open(TRUST_PATH, "r") as f:
            return json.load(f)
    return {"sources": {}, "topics": {}}

def detect_source(text):
    known_sources = ["coindesk", "cointelegraph", "binance", "cryptopanic", "reddit", "twitter", "telegram", "youtube"]
    for src in known_sources:
        if src in text.lower():
            return src
    return "unknown"

def extract_topics(summary):
    keywords = ["elon", "trump", "cz", "panic", "fomo", "etf", "moon", "altseason", "pump"]
    found = []
    for word in keywords:
        if re.search(rf"\b{word}\b", summary.lower()):
            found.append(word)
    return found

def apply_trust_weighting(summary, raw_confidence, trust_config, source=None):
    source = source or detect_source(summary)
    topics = extract_topics(summary)

    source_score = trust_config.get("sources", {}).get(source, DEFAULT_SOURCE_TRUST)
    topic_score = sum([trust_config.get("topics", {}).get(t, DEFAULT_TOPIC_TRUST) for t in topics]) / (len(topics) or 1)

    final_confidence = raw_confidence * source_score * topic_score
    final_confidence = round(min(max(final_confidence, 0), 1), 3)
    return final_confidence, source, topics

def summarize_and_score(text, symbol):
    print(f"[LLM] Summarizing news for {symbol}...")
    trust_config = load_trust_config()

    prompt = f"""Summarize the following crypto-related content for {symbol}.
Return a 3-sentence summary and a confidence score (0 to 1) of how impactful this content is to {symbol}'s price short-term.

Content:
{text[:3000]}
---
Respond in JSON format with "summary" and "confidence".
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        reply = response["choices"][0]["message"]["content"]
        parsed = json.loads(reply)

        summary = parsed.get("summary", "").strip()
        confidence = float(parsed.get("confidence", 0))

        adjusted_confidence, source, topics = apply_trust_weighting(summary, confidence, trust_config)

        print(f"[LLM] Confidence: {confidence} → Adjusted: {adjusted_confidence} | Source: {source} | Topics: {topics}")
        return summary, adjusted_confidence

    except Exception as e:
        print(f"[LLM] Error during summarization: {e}")
        return "Summary failed.", 0.3
