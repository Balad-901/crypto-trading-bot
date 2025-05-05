# telegram/telegram_sender.py

import requests

TELEGRAM_TOKEN = "6870158659:AAGyuwK_9qj2xUXM2iCmrsDz-2Ff_7NjTMg"
TELEGRAM_CHAT_ID = "6578452433"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False
