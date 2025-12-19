from pydantic import BaseModel

class UserSummaryOut(BaseModel):
    proxy_wallet: str
    trades: int
    markets_traded: int
    first_ts: int | None
    last_ts: int | None

class MarketSummaryOut(BaseModel):
    condition_id: str
    trades: int
    traders: int
    first_ts: int | None
    last_ts: int | None
    buy_trades: int
    sell_trades: int
