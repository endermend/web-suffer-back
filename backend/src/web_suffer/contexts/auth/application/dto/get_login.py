from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetLoginInputDTO:
    """InputDTO получения логина пользователя."""

    access_token: str


@dataclass(slots=True, frozen=True)
class GetLoginOutputDTO:
    """OutputDTO получения логина пользователя."""

    email: str
