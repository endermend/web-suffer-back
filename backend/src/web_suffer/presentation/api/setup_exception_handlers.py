from fastapi import FastAPI

from web_suffer.presentation.api.exception_handlers import auth, task


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков исключений по контекстам."""
    auth.setup_exception_handlers(app=app)
    task.setup_exception_handlers(app=app)
