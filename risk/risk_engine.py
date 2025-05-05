# risk/risk_engine.py

import time

trade_cooldowns = {}
trade_history = []

def calculate_position_size(balance, risk_percentage, entry_price, stop_loss_price):
    risk_amount = balance * risk_percentage
    stop_loss_distance = abs(entry_price - stop_loss_price)
    if stop_loss_distance == 0:
        return 0
    quantity = risk_amount / stop_loss_distance
    return round(quantity, 3)

def is_cooldown_active(symbol):
    cooldown_end = trade_cooldowns.get(symbol)
    if cooldown_end is None:
        return False
    return time.time() < cooldown_end

def set_trade_cooldown(symbol, cooldown_seconds=60):
    trade_cooldowns[symbol] = time.time() + cooldown_seconds

def reduce_cooldown(symbol, reduce_seconds=30):
    if symbol in trade_cooldowns:
        trade_cooldowns[symbol] -= reduce_seconds

def record_trade(pnl):
    trade_history.append(pnl)
    if len(trade_history) > 1000:
        trade_history.pop(0)

def get_current_win_rate():
    if not trade_history:
        return 0
    wins = sum(1 for pnl in trade_history if pnl > 0)
    return wins / len(trade_history)

def get_max_drawdown():
    if not trade_history:
        return 0
    peak = trade_history[0]
    max_dd = 0
    for pnl in trade_history:
        if pnl > peak:
            peak = pnl
        drawdown = peak - pnl
        if drawdown > max_dd:
            max_dd = drawdown
    return max_dd
