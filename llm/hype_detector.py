# llm/hype_detector.py

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def detect_hype(text: str):
    # Truncate to 3000 chars to avoid token overload
    text = text.strip()[:3000]

    prompt = """You are a crypto news quality checker.

Analyze the following content and score how hyped, manipulative, or clickbait it is.

Give a score from 0 to 1:
- 0 = no hype, objective and factual
- 1 = extreme hype, emotional, misleading or manipulative

Respond only with a single float value between 0 and 1.

Content:
""" + text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        reply = response.choices[0].message.content.strip()
        return float(reply)
    except Exception as e:
        print(f"[Hype Detection Error] {e}")
        return 0.0
