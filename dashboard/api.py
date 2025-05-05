# dashboard/api.py

from fastapi import APIRouter
from decision.engine import get_bot_status
from monitor.status import get_full_status

router = APIRouter()

@router.get("/dashboard/status")
async def dashboard_status():
    return get_bot_status()

@router.get("/dashboard/metrics")
async def dashboard_metrics():
    return get_full_status()
