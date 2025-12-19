from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Market

class MarketsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        limit: int = 100,
        cursor_condition_id: str | None = None,
        event_id: int | None = None,
        active: bool | None = None,
        closed: bool | None = None,
        archived: bool | None = None,
    ):
        q = select(Market)

        if event_id is not None:
            q = q.where(Market.event_id == event_id)
        if active is not None:
            q = q.where(Market.active == active)
        if closed is not None:
            q = q.where(Market.closed == closed)
        if archived is not None:
            q = q.where(Market.archived == archived)

        # cursor pagination: condition_id is text, so lexicographic cursor is OK for stable paging
        if cursor_condition_id is not None:
            q = q.where(Market.condition_id < cursor_condition_id)

        q = q.order_by(desc(Market.condition_id)).limit(limit)
        res = await self.db.execute(q)
        return res.scalars().all()

    async def get(self, condition_id: str) -> Market | None:
        res = await self.db.execute(select(Market).where(Market.condition_id == condition_id))
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Market | None:
        res = await self.db.execute(select(Market).where(Market.slug == slug))
        return res.scalar_one_or_none()
