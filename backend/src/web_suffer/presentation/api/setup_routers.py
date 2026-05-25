
from fastapi import APIRouter, FastAPI

from web_suffer.presentation.api.routers import auth


def setup_routers(app: FastAPI) -> None:
    """Установка роутеров приложения."""
    api_router = APIRouter(prefix="/api")

    api_router.include_router(auth.router)
    app.include_router(api_router)
