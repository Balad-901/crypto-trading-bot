import json
import os
from datetime import datetime

LOG_FILE = "data/trade_log.json"

def log_trade(symbol, side, quantity, price):
    trade = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "price": price
    }

    os.makedirs("data", exist_ok=True)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            trades = json.load(file)
    else:
        trades = []

    trades.append(trade)

    with open(LOG_FILE, "w") as file:
        json.dump(trades, file, indent=2)

def get_recent_trades(limit=5):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            trades = json.load(file)
            return trades[-limit:]
    return []
