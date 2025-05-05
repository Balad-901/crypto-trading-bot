# summary/llm_summary.py

import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_sentiment(text, symbol):
    prompt = f"""Summarize the following news or content related to {symbol} and provide a confidence score (0 to 1) of its impact on the short-term price.

Text:
{text[:4000]}

Respond in JSON format with "summary" and "confidence".
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        result = response["choices"][0]["message"]["content"]
        data = json.loads(result)
        summary = data.get("summary", "").strip()
        confidence = float(data.get("confidence", 0))
        return summary, confidence
    except Exception as e:
        print("❌ LLM Summary Error:", e)
        return "Summary failed", 0.3
