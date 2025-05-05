# api/routes.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse
import os
import json
import csv
from io import StringIO
from datetime import datetime

router = APIRouter()

TRADES_PATH = "memory/trades.json"
DECISIONS_PATH = "memory/decisions.json"
SENTIMENT_PATH = "memory/sentiment_history.json"
BIAS_LOG_PATH = "logs/biases_log.jsonl"

def load_json(path, fallback=[]):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return fallback

@router.get("/trades")
def get_trades():
    return load_json(TRADES_PATH)

@router.get("/decisions")
def get_decisions():
    return load_json(DECISIONS_PATH)

@router.get("/sentiment")
def get_sentiment():
    return load_json(SENTIMENT_PATH, {})

@router.get("/bias-history")
def get_bias_history():
    entries = []
    if os.path.exists(BIAS_LOG_PATH):
        with open(BIAS_LOG_PATH, "r") as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    continue
    return entries

@router.get("/trades/export")
def export_trades(format: str = Query("csv")):
    trades = load_json(TRADES_PATH)

    if format == "json":
        return JSONResponse(content=trades)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["symbol", "action", "pnl", "confidence", "timestamp"])
    writer.writeheader()
    for t in trades:
        writer.writerow(t)

    filename = f"trades_export_{datetime.utcnow().isoformat()}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
@router.get("/biases")
def get_biases():
    path = "memory/biases.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}
@router.get("/alerts")
def get_alerts():
    path = "logs/alerts.jsonl"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]
@router.get("/bias-history")
def get_bias_history():
    entries = []
    path = "logs/biases_log.jsonl"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except:
                continue
    return entries
