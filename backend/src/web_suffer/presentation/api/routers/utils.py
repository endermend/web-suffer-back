from fastapi import Header

from web_suffer.presentation.exceptions import UnauthorizedCallError


def get_token(authorization: str = Header(...)) -> str:
    """
    Извлекает токен из заголовка Authorization.

    Returns:
        authorization token (access token).

    Raises:
        UnauthorizedCallError: не указан заголовок Authorization.

    """
    if not authorization.startswith("Bearer "):
        raise UnauthorizedCallError
    return authorization.replace("Bearer ", "")
