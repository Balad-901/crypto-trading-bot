portfolio = {
    "balance": 1000.00,  # Starting simulated capital
    "trades": [],
    "risk_level": "medium"
}

def get_balance():
    return round(portfolio["balance"], 2)

def get_risk_level():
    return portfolio["risk_level"]

def update_balance(change):
    portfolio["balance"] += change
    return get_balance()

def get_all_trades():
    return portfolio["trades"]

def log_trade(trade):
    portfolio["trades"].append(trade)
