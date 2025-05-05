# dashboard.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    decisions = load_json("logs/decisions.json")[-10:]  # Show last 10 decisions
    results = load_json("logs/results.json")[-10:]
    cooldown = load_json("logs/cooldown.json") if os.path.exists("logs/cooldown.json") else {}
    weights = load_json("logs/source_weights.json") if os.path.exists("logs/source_weights.json") else {}

    return templates.TemplateResponse("index.html", {
        "request": request,
        "decisions": decisions,
        "results": results,
        "cooldown": cooldown,
        "weights": weights
    })
