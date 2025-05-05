import requests, json, os

TRADE_LOG = "risk/trade_log.json"

def get_price(symbol):
    try:
        url = f"https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}"
        res = requests.get(url).json()
        return float(res["price"])
    except:
        return None

def load_trades():
    if not os.path.exists(TRADE_LOG):
        return []
    with open(TRADE_LOG, "r") as f:
        return json.load(f)

def get_live_pnl():
    trades = load_trades()
    live_pnl = []

    for trade in trades:
        symbol = trade["symbol"]
        side = trade["side"]
        entry = float(trade["entry_price"])
        qty = float(trade["quantity"])
        current = get_price(symbol)

        if not current:
            continue

        # Calculate PnL
        price_diff = current - entry if side == "BUY" else entry - current
        pnl = price_diff * qty
        live_pnl.append({
            "symbol": symbol,
            "side": side,
            "entry": entry,
            "current": current,
            "quantity": qty,
            "pnl": round(pnl, 4)
        })

    return live_pnl
