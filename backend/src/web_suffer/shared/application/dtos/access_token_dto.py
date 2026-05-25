from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AccessTokenDTO:
    """DTO access-токена."""

    access_token: str
