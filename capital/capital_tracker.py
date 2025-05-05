# capital/capital_tracker.py

import json
import os

CAPITAL_FILE = "logs/capital.json"

def initialize_capital(start_amount=100.0):
    if not os.path.exists(CAPITAL_FILE):
        with open(CAPITAL_FILE, "w") as f:
            json.dump({"capital": start_amount}, f)

def get_capital():
    if not os.path.exists(CAPITAL_FILE):
        initialize_capital()
    with open(CAPITAL_FILE, "r") as f:
        return json.load(f)["capital"]

def update_capital(pnl):
    capital = get_capital()
    capital += pnl
    with open(CAPITAL_FILE, "w") as f:
        json.dump({"capital": round(capital, 2)}, f)
    return capital
