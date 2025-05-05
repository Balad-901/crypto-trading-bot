# dashboard/router.py

import io
import matplotlib.pyplot as plt
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import os
from capital.capital_tracker import get_capital, update_capital, initialize_capital

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/api/dashboard")
async def get_dashboard_data():
    try:
        with open("logs/trades.json", "r") as f:
            trades = json.load(f)
    except FileNotFoundError:
        trades = []

    total = len(trades)
    wins = sum(1 for t in trades if t.get("result") == "win")
    avg_conf = sum(t.get("confidence", 0) for t in trades) / total if total > 0 else 0
    pnl = sum(t.get("pnl", 0.0) for t in trades)

    return {
        "total": total,
        "win_rate": round((wins / total) * 100, 2) if total else 0.0,
        "avg_confidence": avg_conf,
        "pnl": pnl,
        "capital": get_capital(),
        "trades": trades[-10:]
    }

@router.get("/dashboard/chart")
async def get_pnl_chart():
    try:
        with open("logs/trades.json", "r") as f:
            trades = json.load(f)
    except FileNotFoundError:
        trades = []

    if not trades:
        trades = [{"pnl": 0.0}]

    x = list(range(1, len(trades) + 1))
    y = [t.get("pnl", 0.0) for t in trades]

    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o", linestyle="-", color="green")
    ax.set_title("Profit / Loss Over Time")
    ax.set_xlabel("Trade #")
    ax.set_ylabel("PnL ($)")
    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@router.post("/reset-capital")
async def reset_capital():
    initialize_capital(100.0)
    return RedirectResponse(url="/dashboard", status_code=302)

@router.post("/withdraw")
async def withdraw(amount: float = Form(...)):
    update_capital(-amount)
    return RedirectResponse(url="/dashboard", status_code=302)
