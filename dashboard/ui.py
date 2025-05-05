# dashboard/ui.py

import os
import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/")
def show_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/api/decisions")
def get_decisions():
    path = os.path.join("memory", "decisions.json")
    if not os.path.exists(path):
        return JSONResponse([])
    with open(path, "r") as f:
        return json.load(f)

@router.get("/api/trades")
def get_trades():
    path = os.path.join("memory", "trades.json")
    if not os.path.exists(path):
        return JSONResponse([])
    with open(path, "r") as f:
        return json.load(f)

@router.get("/api/sentiment")
def get_sentiment_scores():
    path = os.path.join("memory", "sentiment_history.json")
    if not os.path.exists(path):
        return JSONResponse({})
    with open(path, "r") as f:
        return json.load(f)
