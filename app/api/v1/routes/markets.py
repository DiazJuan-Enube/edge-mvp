from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.service.markets_service import MarketsService
from app.schemas.markets import MarketOut, MarketDetailOut

router = APIRouter(prefix="/markets", tags=["markets"])

@router.get("", response_model=list[MarketOut])
async def list_markets(
    limit: int = Query(100, ge=1, le=500),
    cursor_condition_id: str | None = Query(None, description="Return markets with condition_id < cursor_condition_id"),
    event_id: int | None = Query(None),
    active: bool | None = Query(None),
    closed: bool | None = Query(None),
    archived: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = MarketsService(db)
    rows = await svc.list_markets(
        limit=limit,
        cursor_condition_id=cursor_condition_id,
        event_id=event_id,
        active=active,
        closed=closed,
        archived=archived,
    )
    return [
        MarketOut(
            condition_id=r.condition_id,
            event_id=r.event_id,
            slug=r.slug,
            question=r.question,
            active=r.active,
            closed=r.closed,
            archived=r.archived,
        )
        for r in rows
    ]

@router.get("/{condition_id}", response_model=MarketDetailOut)
async def get_market(condition_id: str, db: AsyncSession = Depends(get_db)):
    svc = MarketsService(db)
    row = await svc.get_market(condition_id)
    if not row:
        raise HTTPException(status_code=404, detail="Market not found")
    return MarketDetailOut(
        condition_id=row.condition_id,
        event_id=row.event_id,
        slug=row.slug,
        question=row.question,
        active=row.active,
        closed=row.closed,
        archived=row.archived,
        raw_json=row.raw_json,
    )

@router.get("/by-slug/{slug}", response_model=MarketDetailOut)
async def get_market_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    svc = MarketsService(db)
    row = await svc.get_market_by_slug(slug)
    if not row:
        raise HTTPException(status_code=404, detail="Market not found")
    return MarketDetailOut(
        condition_id=row.condition_id,
        event_id=row.event_id,
        slug=row.slug,
        question=row.question,
        active=row.active,
        closed=row.closed,
        archived=row.archived,
        raw_json=row.raw_json,
    )
