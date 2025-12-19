from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User

class UsersRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, limit: int = 100, cursor_wallet: str | None = None):
        q = select(User)
        if cursor_wallet is not None:
            q = q.where(User.proxy_wallet < cursor_wallet.lower())
        q = q.order_by(desc(User.proxy_wallet)).limit(limit)
        res = await self.db.execute(q)
        return res.scalars().all()

    async def get(self, proxy_wallet: str) -> User | None:
        res = await self.db.execute(select(User).where(User.proxy_wallet == proxy_wallet.lower()))
        return res.scalar_one_or_none()
