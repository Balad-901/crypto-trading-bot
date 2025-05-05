import time
from research.browser_agent import run_browser_research
from llm.summary_agent import summarize_and_store
from utils.symbols import get_trading_symbols  # You should have this list of symbols
import schedule

def research_for_all():
    symbols = get_trading_symbols()
    for symbol in symbols:
        print(f"🔍 Researching: {symbol}")
        results = run_browser_research(symbol)
        for result in results:
            summarize_and_store(result)

# Schedule every hour
schedule.every(1).hours.do(research_for_all)

print("⏱️ Auto research started. Running every hour.")
while True:
    schedule.run_pending()
    time.sleep(10)
