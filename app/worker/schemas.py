from pydantic import BaseModel
from typing import Any, Optional


class TradeMessage(BaseModel):
    condition_id: str
    proxy_wallet: str
    timestamp: int
    transaction_hash: Optional[str]
    side: Optional[str]
    asset: Optional[str]
    outcome: Optional[str]
    outcome_index: Optional[int]
    price: Optional[float]
    size: Optional[float]
    title: Optional[str]
    slug: Optional[str]
    event_slug: Optional[str]
    icon: Optional[str]
    raw: Optional[Any]
