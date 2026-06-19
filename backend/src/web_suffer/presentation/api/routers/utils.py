from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(
    auto_error=True,
    description="JWT токен доступа. Формат: Bearer <token>",
    scheme_name="JWT Authentication",
)

type CredentialsType = Annotated[HTTPAuthorizationCredentials, Depends(security)]
