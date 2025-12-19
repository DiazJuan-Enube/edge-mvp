from pydantic import BaseModel

class EventOut(BaseModel):
    event_id: int
    slug: str | None = None
    title: str | None = None

class EventDetailOut(EventOut):
    raw_json: dict
