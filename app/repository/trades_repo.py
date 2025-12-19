from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Trade

class TradesRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_market(self, condition_id: str, limit: int = 200, cursor_ts: int | None = None):
        q = select(Trade).where(Trade.condition_id == condition_id)
        if cursor_ts is not None:
            q = q.where(Trade.timestamp < cursor_ts)
        q = q.order_by(desc(Trade.timestamp)).limit(limit)
        res = await self.db.execute(q)
        return res.scalars().all()

    async def list_by_user(self, proxy_wallet: str, limit: int = 200, cursor_ts: int | None = None):
        q = select(Trade).where(Trade.proxy_wallet == proxy_wallet)
        if cursor_ts is not None:
            q = q.where(Trade.timestamp < cursor_ts)
        q = q.order_by(desc(Trade.timestamp)).limit(limit)
        res = await self.db.execute(q)
        return res.scalars().all()
