from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.analytics_repo import AnalyticsRepo

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.repo = AnalyticsRepo(db)

    async def user_summary(self, proxy_wallet: str) -> dict:
        return await self.repo.user_summary(proxy_wallet)

    async def market_summary(self, condition_id: str) -> dict:
        return await self.repo.market_summary(condition_id)
