from pydantic import BaseModel

class TradeOut(BaseModel):
    trade_id: int
    condition_id: str
    proxy_wallet: str
    transaction_hash: str | None
    side: str | None
    asset: str | None
    outcome: str | None
    outcome_index: int | None
    price: float | None
    size: float | None
    timestamp: int
    title: str | None
    slug: str | None
    event_slug: str | None
    icon: str | None
