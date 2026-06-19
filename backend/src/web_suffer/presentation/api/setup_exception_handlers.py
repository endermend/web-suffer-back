from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from web_suffer.presentation.api.exception_handlers import auth, task
from web_suffer.presentation.exceptions import UnauthorizedCallError


def unauthorized_user_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    """
    Хэндлер ошибки с форматом почты.

    Returns:
        JSONResponse

    """  # noqa: RUF002
    return JSONResponse(
        content={"detail": "Invalid authorization header"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков исключений по контекстам."""
    app.add_exception_handler(UnauthorizedCallError, unauthorized_user_handler)
    auth.setup_exception_handlers(app=app)
    task.setup_exception_handlers(app=app)
