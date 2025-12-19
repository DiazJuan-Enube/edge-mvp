from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.service.trades_service import TradesService
from app.schemas.trades import TradeOut

router = APIRouter(prefix="/trades", tags=["trades"])

@router.get("/market/{condition_id}", response_model=list[TradeOut])
async def market_trades(
    condition_id: str,
    limit: int = Query(200, ge=1, le=500),
    cursor_ts: int | None = Query(None, description="Return trades with timestamp < cursor_ts"),
    db: AsyncSession = Depends(get_db),
):
    svc = TradesService(db)
    rows = await svc.market_feed(condition_id, limit, cursor_ts)
    return [
        TradeOut(
            trade_id=r.trade_id,
            condition_id=r.condition_id,
            proxy_wallet=r.proxy_wallet,
            transaction_hash=r.transaction_hash,
            side=r.side,
            asset=r.asset,
            outcome=r.outcome,
            outcome_index=r.outcome_index,
            price=float(r.price) if r.price is not None else None,
            size=float(r.size) if r.size is not None else None,
            timestamp=r.timestamp,
            title=r.title,
            slug=r.slug,
            event_slug=r.event_slug,
            icon=r.icon,
        )
        for r in rows
    ]

@router.get("/user/{proxy_wallet}", response_model=list[TradeOut])
async def user_trades(
    proxy_wallet: str,
    limit: int = Query(200, ge=1, le=500),
    cursor_ts: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = TradesService(db)
    rows = await svc.user_history(proxy_wallet, limit, cursor_ts)
    return [
        TradeOut(
            trade_id=r.trade_id,
            condition_id=r.condition_id,
            proxy_wallet=r.proxy_wallet,
            transaction_hash=r.transaction_hash,
            side=r.side,
            asset=r.asset,
            outcome=r.outcome,
            outcome_index=r.outcome_index,
            price=float(r.price) if r.price is not None else None,
            size=float(r.size) if r.size is not None else None,
            timestamp=r.timestamp,
            title=r.title,
            slug=r.slug,
            event_slug=r.event_slug,
            icon=r.icon,
        )
        for r in rows
    ]
