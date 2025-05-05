# data/coinglass.py

from playwright.sync_api import sync_playwright
import re

def fetch_binance_liquidation_zones():
    print("📊 Fetching Binance Coinglass liquidation zones...")
    url = "https://www.coinglass.com/LiquidationData"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)

            # Extract plain body text and look for "Binance" liquidations
            body = page.text_content("body") or ""
            body = body.lower()

            lines = body.splitlines()
            relevant = [line for line in lines if "binance" in line and any(x in line for x in ["long", "short", "usdt"])]

            # Try to extract clusters
            clusters = []
            for line in relevant:
                match = re.findall(r"(long|short).*?(\d+(?:\.\d+)?[kmb]?)", line)
                for direction, amount in match:
                    clusters.append({
                        "exchange": "binance",
                        "type": direction,
                        "amount": amount
                    })

            print(f"📈 Found {len(clusters)} liquidation zones from Binance.")
            return clusters

    except Exception as e:
        print(f"❌ Coinglass fetch error: {e}")
        return []
