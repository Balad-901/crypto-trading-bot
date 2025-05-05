# alerts/telegram.py

import requests
import sys

TELEGRAM_BOT_TOKEN = "7836707618:AAF6qCcHDXPu1tsY5eSub_0AFegTGs_-TFI"
TELEGRAM_CHAT_ID = "7605463011"

def send_telegram_message(message: str):
    print("[DEBUG] Attempting to send Telegram message...", flush=True)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    print(f"[DEBUG] URL: {url}", flush=True)
    print(f"[DEBUG] Payload: {payload}", flush=True)

    try:
        response = requests.post(url, data=payload, timeout=10)
        print(f"[TELEGRAM] Status: {response.status_code}", flush=True)
        print(f"[TELEGRAM] Response: {response.text}", flush=True)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}", file=sys.stderr, flush=True)
