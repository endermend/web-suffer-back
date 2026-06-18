from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from web_suffer.contexts.tasks.application.exceptions import InvalidTaskError


def invalid_task_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    """
    Хэндлер ошибки с отсутсвием задания.

    Returns:
        JSONResponse

    """  # noqa: RUF002
    return JSONResponse(
        content={"detail": "No task present with such id."},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков ошибок."""
    app.add_exception_handler(InvalidTaskError, invalid_task_handler)
