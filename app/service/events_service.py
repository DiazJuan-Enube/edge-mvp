from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.events_repo import EventsRepo

class EventsService:
    def __init__(self, db: AsyncSession):
        self.repo = EventsRepo(db)

    async def list_events(self, limit: int, cursor_event_id: int | None):
        limit = min(max(limit, 1), 500)
        return await self.repo.list(limit=limit, cursor_event_id=cursor_event_id)

    async def get_event(self, event_id: int):
        return await self.repo.get(event_id)

    async def get_event_by_slug(self, slug: str):
        return await self.repo.get_by_slug(slug)
