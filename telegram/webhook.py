from fastapi import APIRouter, Request
from decision.engine import make_decision

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    body = await request.json()
    message = body.get("message", {})
    text = message.get("text", "").strip().lower()

    if text == "/status":
        # TEMP FIX: always use BTCUSDT and 1h timeframe
        result = make_decision(symbol="BTCUSDT", timeframe="1h")
        return {"status": "ok", "decision": result}
    
    return {"status": "ignored", "message": text}
