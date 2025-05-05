import json
import os
from datetime import datetime

LOG_FILE = "logs/strategy_memory.json"

def log_strategy_memory(entry):
    os.makedirs("logs", exist_ok=True)
    entry["timestamp"] = datetime.utcnow().isoformat()

    # Load existing memory
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
