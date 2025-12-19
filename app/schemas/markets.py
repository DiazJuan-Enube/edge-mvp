from pydantic import BaseModel

class MarketOut(BaseModel):
    condition_id: str
    event_id: int | None = None
    slug: str | None = None
    question: str | None = None
    active: bool | None = None
    closed: bool | None = None
    archived: bool | None = None

class MarketDetailOut(MarketOut):
    raw_json: dict
