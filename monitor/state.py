# monitor/state.py

TELEGRAM_BOT_TOKEN = "5927343322:AAEi8dH1-ezLnaS_qA5PhIgGXxWEA3sHuQ0"
TELEGRAM_CHAT_ID = "2164223"

class State:
    def __init__(self):
        self.last_trade_time = None
        self.cooldown_active = False
        self.current_position = None
        self.pnl_history = []

    def to_dict(self):
        return {
            "last_trade_time": str(self.last_trade_time),
            "cooldown_active": self.cooldown_active,
            "current_position": self.current_position,
            "pnl_history": self.pnl_history,
        }

global_state = State()
