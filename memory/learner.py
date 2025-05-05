import json
from memory.strategy_memory import record_result

def learn_from_trades(trade):
    try:
        pnl_value = trade["pnl"]
        if isinstance(pnl_value, dict):
            pnl_value = pnl_value.get("value", 0)

        result = "win" if pnl_value > 0 else "loss"
        symbol = trade.get("symbol", "UNKNOWN")
        strategy_id = trade.get("strategy_id", "default")

        record_result(symbol, strategy_id, result)
        print(f"🧠 Learned from trade: {result}")
    except Exception as e:
        print(f"❌ Learning failed: {e}")
