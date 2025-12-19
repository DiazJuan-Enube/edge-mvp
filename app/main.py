from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import router as v1_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(v1_router)
    return app

app = create_app()
