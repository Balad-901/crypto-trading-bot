import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from openai import OpenAI
import logging

client = OpenAI(api_key="sk-your-key")  # Replace with your key or use system-wide variable

HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_google(query: str, num_results: int = 3):
    encoded_query = quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"] for a in soup.select("a[href^='http']") if "google" not in a["href"]]
    return links[:num_results]

def fetch_article_text(url: str) -> str:
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text.strip()
    except Exception as e:
        logging.error(f"❌ Failed to fetch {url}: {e}")
        return ""

def summarize_with_llm(text: str, max_tokens: int = 500) -> str:
    try:
        chunks = [text[i:i + 3000] for i in range(0, len(text), 3000)]
        summaries = []
        for chunk in chunks:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Summarize the article for a crypto trader."},
                          {"role": "user", "content": chunk}],
                max_tokens=max_tokens,
                temperature=0.5
            )
            summaries.append(completion.choices[0].message.content)
        return "\n\n".join(summaries)
    except Exception as e:
        logging.error(f"❌ LLM summarization failed: {e}")
        return ""

def research_topic(query: str):
    urls = search_google(query)
    results = []
    for url in urls:
        text = fetch_article_text(url)
        summary = summarize_with_llm(text)
        results.append({"url": url, "summary": summary})
    return results
