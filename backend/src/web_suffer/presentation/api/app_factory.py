from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from web_suffer.infrastructure.config import Config
from web_suffer.infrastructure.di.container import make_container_di
from web_suffer.infrastructure.seeders.superadmin_seeder import SuperAdminSeeder
from web_suffer.presentation.api.setup_exception_handlers import setup_exception_handlers
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
    container = make_container_di(config=config)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None,]:
        await _run_seeders(container)
        yield
        await container.close()

    app = FastAPI(lifespan=lifespan)

    # Middleware
    setup_middleware(app=app)

    # Routers
    setup_routers(app=app)

    # Exception handlers
    setup_exception_handlers(app=app)

    # Dishka
    setup_dishka(container=container, app=app)

    return app


async def _run_seeders(container: AsyncContainer) -> None:
    async with container() as request_container:
        seeder = await request_container.get(SuperAdminSeeder)
        await seeder.seed()
