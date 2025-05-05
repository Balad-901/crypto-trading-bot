# dashboard/viewer.py

import json
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

def load_trades():
    try:
        with open("trades.json", "r") as f:
            return json.load(f)
    except:
        return []

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    trades = load_trades()
    rows = ""
    pnl = 0
    for t in trades:
        result = t.get("result", "")
        if result == "win":
            pnl += 10  # Simulate +10 per win
        elif result == "loss":
            pnl -= 10  # Simulate -10 per loss

        rows += f"""
        <tr>
            <td>{t.get("symbol")}</td>
            <td>{t.get("timeframe")}</td>
            <td>{t.get("decision")}</td>
            <td>{t.get("confidence"):.2f}</td>
            <td>{t.get("result", "-")}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Trading Bot Dashboard</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #111; color: white; }}
            h2 {{ font-family: sans-serif }}
        </style>
    </head>
    <body>
        <h2>📈 Bot Dashboard</h2>
        <p><b>Simulated PnL:</b> {pnl} USDT</p>
        <table>
            <tr>
                <th>Symbol</th>
                <th>Timeframe</th>
                <th>Decision</th>
                <th>Confidence</th>
                <th>Result</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
