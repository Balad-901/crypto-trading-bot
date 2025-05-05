# memory/strategy_memory.py

import os
import json

def get_strategy_confidence_boost(symbol, signal, timeframe):
    path = "logs/strategy_memory.json"
    if not os.path.exists(path):
        return 0
    with open(path, "r") as f:
        memory = json.load(f)
    key = f"{symbol}_{signal}_{timeframe}"
    stats = memory.get(key, {"wins": 0, "losses": 0})
    total = stats["wins"] + stats["losses"]
    if total == 0:
        return 0
    return round((stats["wins"] / total) * 10, 2)

def update_strategy_memory(symbol, signal, timeframe, result):
    path = "logs/strategy_memory.json"
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if os.path.exists(path):
        with open(path, "r") as f:
            memory = json.load(f)
    else:
        memory = {}
    key = f"{symbol}_{signal}_{timeframe}"
    if key not in memory:
        memory[key] = {"wins": 0, "losses": 0}
    memory[key]["wins" if result == "win" else "losses"] += 1
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def record_result(symbol, signal, timeframe, result):
    update_strategy_memory(symbol, signal, timeframe, result)
