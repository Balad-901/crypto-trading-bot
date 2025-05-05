from fastapi import APIRouter, Request
from decision.engine import make_decision
from utils.logger import log_event

router = APIRouter()

@router.post("/webhook")
async def webhook_handler(request: Request):
    try:
        payload = await request.json()
        symbol = payload.get("symbol", "BTCUSDT")
        signal = payload.get("signal", "buy")
        timeframe = payload.get("timeframe", "15m")

        decision = make_decision(symbol, signal, timeframe)

        log_event("decisions.json", decision)
        return {"status": "success", "decision": decision}

    except Exception as e:
        log_event("errors.json", {"error": str(e)})
        return {"status": "error", "message": str(e)}
