from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from web_suffer.shared.domain.exceptions import DomainError, InsufficientPermissionsError


def base_domain_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    """
    Хэндлер базовой ошибки домена.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "Unprocessable domain error id."},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


def insufficient_premission_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    """
    Хэндлер ошибки нехватки прав.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "User does not have enought rights."},
        status_code=status.HTTP_403_FORBIDDEN,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков ошибок."""
    app.add_exception_handler(DomainError, base_domain_handler)
    app.add_exception_handler(InsufficientPermissionsError, insufficient_premission_handler)
