from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.service.events_service import EventsService
from app.schemas.events import EventOut, EventDetailOut

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=list[EventOut])
async def list_events(
    limit: int = Query(100, ge=1, le=500),
    cursor_event_id: int | None = Query(None, description="Return events with event_id < cursor_event_id"),
    db: AsyncSession = Depends(get_db),
):
    svc = EventsService(db)
    rows = await svc.list_events(limit, cursor_event_id)
    return [EventOut(event_id=r.event_id, slug=r.slug, title=r.title) for r in rows]

@router.get("/{event_id}", response_model=EventDetailOut)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventsService(db)
    row = await svc.get_event(event_id)
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventDetailOut(event_id=row.event_id, slug=row.slug, title=row.title, raw_json=row.raw_json)

@router.get("/by-slug/{slug}", response_model=EventDetailOut)
async def get_event_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    svc = EventsService(db)
    row = await svc.get_event_by_slug(slug)
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventDetailOut(event_id=row.event_id, slug=row.slug, title=row.title, raw_json=row.raw_json)
