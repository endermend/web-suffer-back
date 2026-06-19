from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AccessTokenDTO:
    """DTO access-токена."""

    access_token: str


@dataclass(slots=True, frozen=True)
class PublicAccessTokenDTO:
    """DTO access-токена для публичного эндпоинта."""

    access_token: str | None
