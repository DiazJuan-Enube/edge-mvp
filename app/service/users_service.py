from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.users_repo import UsersRepo

class UsersService:
    def __init__(self, db: AsyncSession):
        self.repo = UsersRepo(db)

    async def list_users(self, limit: int = 100, cursor_wallet: str | None = None):
        return await self.repo.list(limit=limit, cursor_wallet=cursor_wallet)

    async def get_user(self, proxy_wallet: str):
        return await self.repo.get(proxy_wallet)
