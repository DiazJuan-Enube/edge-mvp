from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class AnalyticsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def user_summary(self, proxy_wallet: str) -> dict:
        q = text("""
          select
            count(*)::bigint as trades,
            count(distinct condition_id)::bigint as markets_traded,
            min(timestamp)::bigint as first_ts,
            max(timestamp)::bigint as last_ts
          from trades
          where proxy_wallet = :w
        """)
        res = await self.db.execute(q, {"w": proxy_wallet.lower()})
        return dict(res.mappings().one())

    async def market_summary(self, condition_id: str) -> dict:
        q = text("""
          select
            count(*)::bigint as trades,
            count(distinct proxy_wallet)::bigint as traders,
            min(timestamp)::bigint as first_ts,
            max(timestamp)::bigint as last_ts,
            sum(case when side = 'BUY' then 1 else 0 end)::bigint as buy_trades,
            sum(case when side = 'SELL' then 1 else 0 end)::bigint as sell_trades
          from trades
          where condition_id = :cid
        """)
        res = await self.db.execute(q, {"cid": condition_id})
        return dict(res.mappings().one())
