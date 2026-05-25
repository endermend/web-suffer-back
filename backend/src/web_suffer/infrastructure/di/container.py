from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from web_suffer.contexts.auth.infrastructure.di.auth_provider import AuthProvider
from web_suffer.infrastructure.config import Config


def make_container_di(config: Config) -> AsyncContainer:
    """
    Создание асинхронного контейнера.

    Returns:
        AsyncContainer

    """
    return make_async_container(
        AuthProvider(),
        FastapiProvider(),
        context={Config: config},
    )
