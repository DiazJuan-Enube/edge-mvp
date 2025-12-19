from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.service.analytics_service import AnalyticsService
from app.schemas.analytics import UserSummaryOut, MarketSummaryOut

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/user/{proxy_wallet}/summary", response_model=UserSummaryOut)
async def user_summary(proxy_wallet: str, db: AsyncSession = Depends(get_db)):
    svc = AnalyticsService(db)
    s = await svc.user_summary(proxy_wallet)
    # if user has no trades, counts will be 0 but row still returns; that's OK.
    return UserSummaryOut(proxy_wallet=proxy_wallet.lower(), **s)

@router.get("/market/{condition_id}/summary", response_model=MarketSummaryOut)
async def market_summary(condition_id: str, db: AsyncSession = Depends(get_db)):
    svc = AnalyticsService(db)
    s = await svc.market_summary(condition_id)
    if s["trades"] == 0:
        # might still be a valid market with 0 trades, but most people prefer a 404 here
        raise HTTPException(status_code=404, detail="No trades found for this market (or market unknown)")
    return MarketSummaryOut(condition_id=condition_id, **s)
