# risk/cooldown_manager.py

import time

COOLDOWN_STATE = {
    "active": False,
    "until": 0
}

def trigger_cooldown(minutes=10):
    COOLDOWN_STATE["active"] = True
    COOLDOWN_STATE["until"] = time.time() + (minutes * 60)
    print(f"🚫 Cooldown activated for {minutes} minutes.")

def check_cooldown():
    if COOLDOWN_STATE["active"]:
        if time.time() > COOLDOWN_STATE["until"]:
            COOLDOWN_STATE["active"] = False
            print("✅ Cooldown expired, resuming normal trading.")
        else:
            print("🚫 Still in cooldown period, skipping trade.")
            return True
    return False
