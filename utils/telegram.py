# utils/telegram.py

import requests

TELEGRAM_BOT_TOKEN = "7836707618:AAF6qCcHDXPu1tsY5eSub_0AFegTGs_-TFI"
TELEGRAM_CHAT_ID = "6973933102"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Telegram send error: {e}")
