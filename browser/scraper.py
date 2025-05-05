# browser/scraper.py

from playwright.sync_api import sync_playwright

NEWS_SOURCES = {
    "CoinDesk": "https://www.coindesk.com",
    "CoinTelegraph": "https://www.cointelegraph.com",
    "RedditCrypto": "https://www.reddit.com/r/CryptoCurrency/",
    "BinanceBlog": "https://www.binance.com/en/feed",
    "CryptoSlate": "https://cryptoslate.com/",
    "CoinMarketCap": "https://coinmarketcap.com/headlines/news/"
}

# Enhanced synonym dictionary for fuzzy keyword matching
KEYWORD_ALIASES = {
    "BTC": ["btc", "bitcoin", "btc-usdt", "btc/usdt"],
    "BTCUSDT": ["btc", "bitcoin", "btc-usdt", "btc/usdt"],
    "ETH": ["eth", "ethereum", "eth-usdt", "eth/usdt"],
    "ETHUSDT": ["eth", "ethereum", "eth-usdt", "eth/usdt"],
    "ADA": ["ada", "cardano", "ada-usdt", "ada/usdt"],
    "HBAR": ["hbar", "hedera", "hbar-usdt", "hbar/usdt"],
    "PIXEL": ["pixel", "pixels", "pixel/usdt", "pixel token"],
    "ARB": ["arb", "arbitrum", "arb-usdt", "arb/usdt"],
    "XRP": ["xrp", "ripple", "xrp-usdt", "xrp/usdt"],
    "SOL": ["sol", "solana", "sol/usdt", "sol-usdt"],
    "BNB": ["bnb", "binance coin", "bnb-usdt", "bnb/usdt"],
    "DOGE": ["doge", "dogecoin", "doge-usdt", "doge/usdt"],
    "MATIC": ["matic", "polygon", "matic-usdt", "matic/usdt"],
    "DOT": ["dot", "polkadot", "dot-usdt", "dot/usdt"],
    "SHIB": ["shib", "shiba inu", "shib-usdt", "shib/usdt"],
    "AVAX": ["avax", "avalanche", "avax-usdt", "avax/usdt"],
    "LINK": ["link", "chainlink", "link-usdt", "link/usdt"],
    "LTC": ["ltc", "litecoin", "ltc-usdt", "ltc/usdt"],
    "TRX": ["trx", "tron", "trx-usdt", "trx/usdt"],
    "ATOM": ["atom", "cosmos", "atom-usdt", "atom/usdt"],
    "APT": ["apt", "aptos", "apt-usdt", "apt/usdt"]
}

def search_web(symbol: str):
    print(f"🌐 Browsing for: {symbol} news...")
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        aliases = KEYWORD_ALIASES.get(symbol.upper(), [symbol.lower()])

        for name, url in NEWS_SOURCES.items():
            try:
                print(f"🔎 Visiting {name}: {url}")
                page.goto(url, timeout=60000)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)

                body = page.text_content("body") or ""
                body = body.replace("\n\n", "\n")
                paragraphs = body.split("\n")

                snippets = [
                    line.strip()
                    for line in paragraphs
                    if any(alias in line.lower() for alias in aliases) and 40 < len(line.strip()) < 300
                ]

                for s in snippets[:3]:
                    results.append({
                        "source": name,
                        "snippet": s
                    })

            except Exception as e:
                print(f"❌ Error scraping {name}: {e}")

        browser.close()

    return results
