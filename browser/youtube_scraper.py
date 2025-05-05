# browser/youtube_scraper.py

import asyncio
from playwright.sync_api import sync_playwright

def scrape_youtube_videos(query, max_results=5):
    videos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+crypto"
        page.goto(search_url, timeout=60000)

        page.wait_for_selector("ytd-video-renderer", timeout=10000)

        results = page.query_selector_all("ytd-video-renderer")

        for r in results[:max_results]:
            title = r.query_selector("a#video-title")
            link = title.get_attribute("href")
            views = r.query_selector("span.inline-metadata-item")
            description = r.query_selector("yt-formatted-string#description-text")

            videos.append({
                "title": title.inner_text().strip() if title else "",
                "url": f"https://www.youtube.com{link}" if link else "",
                "views": views.inner_text().strip() if views else "",
                "description": description.inner_text().strip() if description else "",
            })

        browser.close()

    return videos

# Test
if __name__ == "__main__":
    results = scrape_youtube_videos("bitcoin etf")
    for r in results:
        print(f"{r['title']} ({r['views']})\n{r['url']}\n{r['description']}\n")
