from fastapi import FastAPI

from web_suffer.config import Config
from web_suffer.contexts.auth.presentation.api import (
    setup_exception_handlers,
    setup_routers,
)
from web_suffer.contexts.auth.presentation.api.middleware import setup_middleware
from web_suffer.contexts.auth.presentation.dependencies import setup_di


def create_app() -> FastAPI:
    """
    Создание приложения FastAPI.

    Создается приложение FastAPI, подключаются middleware, routers,
    exception handlers и di

    Returns:
        FastAPI

    """
    config = Config()  # pyright: ignore[reportCallIssue] # ty:ignore[missing-argument]

    app = FastAPI()

    setup_middleware(app=app)
    setup_routers(app=app)
    setup_exception_handlers(app=app)
    setup_di(app=app, config=config)

    return app
