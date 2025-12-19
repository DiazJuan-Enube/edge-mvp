from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.transactions_repo import TransactionsRepo

class TransactionsService:
    def __init__(self, db: AsyncSession):
        self.repo = TransactionsRepo(db)

    async def market_feed(self, condition_id: str, limit: int, cursor_ts: int | None):
        limit = min(max(limit, 1), 500)
        return await self.repo.list_by_market(condition_id, limit=limit, cursor_ts=cursor_ts)

    async def user_history(self, proxy_wallet: str, limit: int, cursor_ts: int | None):
        limit = min(max(limit, 1), 500)
        return await self.repo.list_by_user(proxy_wallet.lower(), limit=limit, cursor_ts=cursor_ts)
