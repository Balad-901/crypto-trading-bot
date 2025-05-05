# utils/symbol_manager.py

ALLOWED_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT",
    "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "MATICUSDT", "SUIUSDT",
    "PEPEUSDT", "ARBUSDT", "PIXELUSDT", "HBARUSDT"
]

def is_valid_symbol(symbol):
    return symbol in ALLOWED_SYMBOLS

def add_new_symbol(symbol):
    if symbol not in ALLOWED_SYMBOLS:
        ALLOWED_SYMBOLS.append(symbol)
        print(f"✅ New symbol {symbol} added to allowed list.")
