import asyncio

from app.db import models
from app.db.session import engine


async def init_models() -> None:
    """Create all tables from SQLAlchemy models using the async engine."""
    async with engine.begin() as conn:
        # run_sync allows calling SQLAlchemy metadata.create_all in sync mode
        await conn.run_sync(models.Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_models())
    print("Database tables created (or already existed).")
