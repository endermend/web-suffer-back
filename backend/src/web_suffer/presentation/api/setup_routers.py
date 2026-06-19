from fastapi import APIRouter, FastAPI

from web_suffer.presentation.api.routers import auth, download, task


def setup_routers(app: FastAPI) -> None:
    """Установка роутеров приложения."""
    api_router = APIRouter(prefix="/api")

    api_router.include_router(auth.router)
    api_router.include_router(task.router)
    api_router.include_router(download.router)
    app.include_router(api_router)
