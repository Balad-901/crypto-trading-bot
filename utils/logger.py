# utils/logger.py

import json
import os
from datetime import datetime

def log_event(filename, data):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, filename)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []

    existing.append(log_entry)

    with open(path, "w") as f:
        json.dump(existing, f, indent=2)
