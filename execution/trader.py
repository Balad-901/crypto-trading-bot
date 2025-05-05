# execution/trader.py

import os
import json
import time
from datetime import datetime

COOLDOWN_SECONDS = 1800  # 30 mins cooldown per symbol
STOP_LOSS = -5.0         # -5% PnL
TAKE_PROFIT = 10.0       # +10% PnL

cooldowns = {}
open_trades = {}

def is_in_cooldown(symbol):
    last_time = cooldowns.get(symbol)
    if last_time and (time.time() - last_time) < COOLDOWN_SECONDS:
        return True
    return False

def simulate_trade(symbol, confidence):
    if is_in_cooldown(symbol):
        print(f"⏳ Cooldown active for {symbol}")
        return None

    # Simulate fake PnL based on confidence
    fake_pnl = round(confidence * 20 - 5, 2)  # e.g. 0.6 → 7%, 0.3 → 1%

    # Check SL/TP logic
    if fake_pnl >= TAKE_PROFIT:
        outcome = "take_profit"
    elif fake_pnl <= STOP_LOSS:
        outcome = "stop_loss"
    else:
        outcome = "hold"

    trade = {
        "symbol": symbol,
        "confidence": confidence,
        "pnl": fake_pnl,
        "outcome": outcome,
        "timestamp": datetime.utcnow().isoformat()
    }

    log_trade(trade)
    cooldowns[symbol] = time.time()
    open_trades[symbol] = trade
    print(f"📈 Simulated trade for {symbol} → PnL: {fake_pnl}%, outcome: {outcome}")
    return trade

def log_trade(trade):
    path = os.path.join("memory", "trades.json")
    trades = []
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                trades = json.load(f)
            except:
                pass
    trades.append(trade)
    with open(path, "w") as f:
        json.dump(trades, f, indent=2)
