from playwright.sync_api import sync_playwright
from llm.summary_agent import summarize_and_store

def run_browser_research():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        keywords = ["bitcoin etf", "crypto regulation", "altcoin news"]

        for keyword in keywords:
            print(f"\n🔍 Searching for: {keyword}")
            page.goto(f"https://duckduckgo.com/?q={keyword}&t=h_&ia=web")
            page.wait_for_timeout(3000)
            links = page.eval_on_selector_all("a.result__a", "elements => elements.map(el => el.href)")
            top_links = links[:3]
            for link in top_links:
                summarize_and_store(link)

        browser.close()
