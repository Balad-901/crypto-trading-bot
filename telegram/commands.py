# telegram/commands.py

import json
import os
import requests

TELEGRAM_TOKEN = "7836707618:AAF6qCcHDXPu1tsY5eSub_0AFegTGs_-TFI"
CHAT_ID = "7605463011"
STATE_FILE = "bot_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"paused": False}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def is_paused():
    return load_state().get("paused", False)

def handle_command(text):
    state = load_state()
    response = ""

    if "/status" in text:
        paused = state.get("paused", False)
        response = "⏸️ Bot is PAUSED" if paused else "✅ Bot is ACTIVE"

    elif "/pause" in text:
        state["paused"] = True
        save_state(state)
        response = "🛑 Bot has been PAUSED"

    elif "/resume" in text:
        state["paused"] = False
        save_state(state)
        response = "▶️ Bot has been RESUMED"

    else:
        response = "🤖 Unknown command"

    send_message(response)

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[TELEGRAM] Failed to send command response: {e}")
