from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.service.users_service import UsersService
from app.schemas.users import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
async def list_users(
    limit: int = Query(100, ge=1, le=500),
    cursor_wallet: str | None = Query(None, description="Return users with proxy_wallet < cursor_wallet"),
    db: AsyncSession = Depends(get_db),
):
    svc = UsersService(db)
    rows = await svc.list_users(limit, cursor_wallet)
    return [
        UserOut(
            proxy_wallet=r.proxy_wallet,
            name=r.name,
            profile_image=r.profile_image,
            first_seen_ts=r.first_seen_ts,
            last_seen_ts=r.last_seen_ts,
        )
        for r in rows
    ]

@router.get("/{proxy_wallet}", response_model=UserOut)
async def get_user(proxy_wallet: str, db: AsyncSession = Depends(get_db)):
    svc = UsersService(db)
    row = await svc.get_user(proxy_wallet)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        proxy_wallet=row.proxy_wallet,
        name=row.name,
        profile_image=row.profile_image,
        first_seen_ts=row.first_seen_ts,
        last_seen_ts=row.last_seen_ts,
    )
