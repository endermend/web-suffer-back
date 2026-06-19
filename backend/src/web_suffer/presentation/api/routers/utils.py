from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(
    auto_error=False,
    description="JWT токен доступа. Формат: Bearer <token>",
    scheme_name="JWT Authentication",
)

# Тип, который может быть None
type OptionalCredentialsType = Annotated[HTTPAuthorizationCredentials | None, Depends(security)]


def require_auth(credentials: OptionalCredentialsType) -> HTTPAuthorizationCredentials:
    """
    Проверяет наличие токена и возвращает его или выбрасывает 403.

    Returns:
        HTTPAuthorizationCredentials: обязательные credentials.

    Raises:
        HTTPException: 403, если credentials не указаны.

    """  # noqa: RUF002
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


type CredentialsType = Annotated[HTTPAuthorizationCredentials, Depends(require_auth)]
