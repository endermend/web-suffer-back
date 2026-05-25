from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AccessTokenDTO:
    """DTO access-токена."""

    access_token: str


@dataclass(slots=True, frozen=True)
class RefreshTokenDTO:
    """DTO refresh-токена."""

    refresh_token: str


@dataclass(slots=True, frozen=True)
class TokensDTO:
    """DTO токенов."""

    access_token: str
    refresh_token: str
