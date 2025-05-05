from llm.summary_agent import fetch_article_text, summarize_article, store_summary

url = "https://www.cbsnews.com/news/bitcoin-etf-sec-approval-impact/"
print(f"🔗 Fetching article: {url}")

text = fetch_article_text(url)
print(f"📄 Text preview (first 300 chars):\n{text[:300]}")

print("🧠 Summarizing with OpenAI...")
summary = summarize_article(text)
print(f"\n📝 Summary:\n{summary}")

print("💾 Saving to memory...")
store_summary(url, summary)
print("✅ Done.")
