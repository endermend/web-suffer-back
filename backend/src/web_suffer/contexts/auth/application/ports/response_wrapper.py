from typing import Literal, Protocol


class ResponseWrapper(Protocol):
    """Абстракция над HTTP-ответом. Чистая, без FastAPI."""

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
        """Установка значения в куки по ключу."""

    def delete_cookie(
        self,
        key: str,
        path: str = "/",
        secure: bool = False,  # noqa: FBT001, FBT002
        httponly: bool = False,  # noqa: FBT001, FBT002
        samesite: Literal["lax", "strict", "none"] | None = None,
    ) -> None:
        """Удаление значения куки по ключу."""
