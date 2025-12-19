from pydantic import BaseModel

class UserOut(BaseModel):
    proxy_wallet: str
    name: str | None = None
    profile_image: str | None = None
    first_seen_ts: int | None = None
    last_seen_ts: int | None = None
