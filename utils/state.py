import time

bot_status = {
    "capital": 10000,
    "last_trade_time": 0,
    "cooldown_seconds": 60,  # Cooldown after a trade (1 minute default)
    "open_position": False
}

def get_bot_status():
    return bot_status

def update_bot_capital(amount):
    bot_status["capital"] += amount

def set_last_trade_time():
    bot_status["last_trade_time"] = time.time()

def can_trade_now():
    return time.time() - bot_status["last_trade_time"] >= bot_status["cooldown_seconds"]

def set_open_position(opened: bool):
    bot_status["open_position"] = opened
