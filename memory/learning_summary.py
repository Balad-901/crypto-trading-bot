import json
import os

CONFIDENCE_FILE = "memory/confidence_learning.json"

def summarize_learning():
    if not os.path.exists(CONFIDENCE_FILE):
        return "No confidence learning data yet."

    with open(CONFIDENCE_FILE, "r") as f:
        data = json.load(f)

    summary_lines = []
    for key, values in data.items():
        total = values.get("total", 0)
        success = values.get("success", 0)
        win_rate = round((success / total) * 100, 2) if total > 0 else 0.0
        summary_lines.append(
            f"• {key}: {success}/{total} wins ({win_rate}%)"
        )

    return "\n".join(summary_lines)
