from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.markets_repo import MarketsRepo

class MarketsService:
    def __init__(self, db: AsyncSession):
        self.repo = MarketsRepo(db)

    async def list_markets(self, limit: int, cursor_condition_id: str | None, **filters):
        limit = min(max(limit, 1), 500)
        return await self.repo.list(limit=limit, cursor_condition_id=cursor_condition_id, **filters)

    async def get_market(self, condition_id: str):
        return await self.repo.get(condition_id)

    async def get_market_by_slug(self, slug: str):
        return await self.repo.get_by_slug(slug)
