# utils/pnl_tracker.py

import json
import os
from datetime import datetime
import random

TRADE_LOG = "logs/trades.json"
os.makedirs("logs", exist_ok=True)

def load_trades():
    if not os.path.exists(TRADE_LOG):
        return []
    with open(TRADE_LOG, "r") as f:
        return json.load(f)

def save_trade(entry):
    trades = load_trades()
    trades.append(entry)
    with open(TRADE_LOG, "w") as f:
        json.dump(trades, f, indent=2)

def simulate_trade(symbol, action, confidence):
    """Simulate a trade outcome (for now), replace later with real Binance result."""
    pnl = round(random.uniform(-0.05, 0.10) * confidence, 4)  # simulate +/- 5–10% based on confidence
    result = {
        "symbol": symbol,
        "action": action,
        "confidence": confidence,
        "pnl": pnl,
        "timestamp": datetime.utcnow().isoformat()
    }
    save_trade(result)
    print(f"💰 Trade simulated: {symbol} {action} → PnL: {pnl}")
    return pnl

def average_pnl(symbol):
    trades = load_trades()
    symbol_trades = [t for t in trades if t["symbol"] == symbol]
    if not symbol_trades:
        return 0
    return round(sum(t["pnl"] for t in symbol_trades) / len(symbol_trades), 4)
