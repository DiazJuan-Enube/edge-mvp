from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Event

class EventsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, limit: int = 100, cursor_event_id: int | None = None):
        q = select(Event)
        if cursor_event_id is not None:
            q = q.where(Event.event_id < cursor_event_id)
        q = q.order_by(desc(Event.event_id)).limit(limit)
        res = await self.db.execute(q)
        return res.scalars().all()

    async def get(self, event_id: int) -> Event | None:
        res = await self.db.execute(select(Event).where(Event.event_id == event_id))
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Event | None:
        res = await self.db.execute(select(Event).where(Event.slug == slug))
        return res.scalar_one_or_none()
