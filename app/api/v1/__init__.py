from fastapi import APIRouter

from .routes.health import router as health_router
from .routes.events import router as events_router
from .routes.markets import router as markets_router
from .routes.users import router as users_router
from .routes.trades import router as trades_router
from .routes.analytics import router as analytics_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(events_router)
router.include_router(markets_router)
router.include_router(users_router)
router.include_router(trades_router)
router.include_router(analytics_router)
