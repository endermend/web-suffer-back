from typing import Literal

from fastapi import Response

from web_suffer.contexts.auth.application.ports.response_wrapper import ResponseWrapper


class FastAPIResponseAdapter(ResponseWrapper):
    """Адаптер: FastAPI Response."""

    def __init__(self, response: Response) -> None:
        """Настройка адаптера."""
        self._response = response

    def set_cookie(  # noqa: PLR0913, PLR0917
        self,
        key: str,
        value: str,
        max_age: int | None = None,
        secure: bool = False,  # noqa: FBT001, FBT002
        httponly: bool = False,  # noqa: FBT001, FBT002
        samesite: Literal["lax", "strict", "none"] | None = None,
        path: str = "/",
    ) -> None:
        """Установка куки."""
        self._response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
            path=path,
        )

    def delete_cookie(
        self,
        key: str,
        path: str = "/",
        secure: bool = False,  # noqa: FBT001, FBT002
        httponly: bool = False,  # noqa: FBT001, FBT002
        samesite: Literal["lax", "strict", "none"] | None = None,
    ) -> None:
        """Удаление куки."""
        self._response.delete_cookie(
            key=key,
            path=path,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
        )
