# logger.py

import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(filename, data):
    path = os.path.join(LOG_DIR, filename)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data
    }

    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([log_entry], f, indent=2)
    else:
        with open(path, "r+") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

            existing.append(log_entry)
            f.seek(0)
            json.dump(existing, f, indent=2)
            f.truncate()
