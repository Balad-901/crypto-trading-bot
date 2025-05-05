import requests, time, hmac, hashlib

API_KEY = "c75e1e33e4815517a57dc5b5662a3292041de7dbf5f6b0dbb9a05ea9aaa93346"
API_SECRET = "adf448fa9240357f09fdd778aa7dcc638a49312d0c8a98c8c91ceb7d5cc44469"
BASE_URL = "https://testnet.binancefuture.com"

LAST_TRADE_TIME = 0
COOLDOWN_SECONDS = 60

def sign_request(params):
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return query + f"&signature={signature}"

def place_test_order(symbol, side, capital_usd=1000):
    global LAST_TRADE_TIME
    now = time.time()
    if now - LAST_TRADE_TIME < COOLDOWN_SECONDS:
        print("⏳ Cooldown active, skipping order")
        return

    # Entry price fetch (mocked or replace with Binance price API later)
    entry_price = 50000 if "BTC" in symbol else 1.0
    quantity = round(capital_usd / entry_price, 4)

    endpoint = "/fapi/v1/order"
    url = BASE_URL + endpoint

    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000)
    }

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    query = sign_request(params)
    try:
        response = requests.post(url + "?" + query, headers=headers)
        print("✅ Order Response:", response.json())
    except Exception as e:
        print("❌ Order failed:", str(e))

    # SL/TP (mocked for now — for real SL/TP you'd use conditional orders)
    sl_price = entry_price * (0.98 if side.lower() == "buy" else 1.02)
    tp_price = entry_price * (1.05 if side.lower() == "buy" else 0.95)

    print(f"🛑 Stop Loss: {sl_price:.2f} | 🎯 Take Profit: {tp_price:.2f}")

    LAST_TRADE_TIME = now
