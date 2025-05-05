# memory/trade_history.py

import json
import os
from typing import Optional

TRADE_HISTORY_FILE = "logs/results.json"

def load_trade_history():
    if not os.path.exists(TRADE_HISTORY_FILE):
        return []
    with open(TRADE_HISTORY_FILE, "r") as f:
        return json.load(f)

def save_trade_result(result: dict):
    history = load_trade_history()
    history.append(result)
    with open(TRADE_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def evaluate_trade(entry_price: float, exit_price: float, position_size: float) -> dict:
    profit = round((exit_price - entry_price) * (position_size / entry_price), 2)
    outcome = "win" if profit > 0 else "loss" if profit < 0 else "neutral"
    percent_return = round((exit_price - entry_price) / entry_price * 100, 2)

    return {
        "entry": entry_price,
        "exit": exit_price,
        "size": position_size,
        "pnl": profit,
        "return_percent": percent_return,
        "result": outcome
    }

def calculate_win_rate() -> Optional[float]:
    history = load_trade_history()
    if not history:
        return None
    wins = sum(1 for t in history if t["result"] == "win")
    return round(wins / len(history) * 100, 2)
