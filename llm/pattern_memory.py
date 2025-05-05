# llm/pattern_memory.py

import os
import openai
import json
from memory.writer import save_pattern_summary

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_patterns(memory_data):
    prompt = f"""You are a crypto trading strategist. Analyze the following research memory to detect repeating patterns, influencers, or events that have affected market sentiment or prices across multiple tokens. Give a short plain-language summary of your findings.

Data:
{json.dumps(memory_data)[:4000]}
"""

    try:
        print("🔎 Analyzing memory patterns...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        summary = response["choices"][0]["message"]["content"]
        print("✅ Pattern summary generated.")
        return summary
    except Exception as e:
        print("❌ Error during pattern analysis:", e)
        return "Pattern analysis failed."

def run_pattern_learning():
    print("📊 Running pattern memory...")
    if not os.path.exists("memory/research_memory.json"):
        print("No research memory found.")
        return

    with open("memory/research_memory.json", "r") as f:
        memory_data = json.load(f)

    summary = analyze_patterns(memory_data)
    save_pattern_summary(summary)

if __name__ == "__main__":
    run_pattern_learning()
