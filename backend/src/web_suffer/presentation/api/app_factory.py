from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from web_suffer.infrastructure.config import Config
from web_suffer.infrastructure.di.container import make_container_di
from web_suffer.presentation.api.exception_handlers import auth
from web_suffer.presentation.api.setup_middleware import setup_middleware
from web_suffer.presentation.api.setup_routers import setup_routers


def create_app() -> FastAPI:
    """
    Создание приложения FastAPI.

    Создается приложение FastAPI, подключаются middleware, routers,
    exception handlers и di

    Returns:
        FastAPI

    """
    config = Config()  # ty:ignore[missing-argument]

    app = FastAPI()

    # Middleware
    setup_middleware(app=app)

    # Routers
    setup_routers(app=app)

    # Exception handlers
    auth.setup_exception_handlers(app=app)

    # Dishka
    container = make_container_di(config=config)
    setup_dishka(container=container, app=app)

    return app
