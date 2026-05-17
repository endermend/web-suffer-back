from web_suffer.shared.application.exceptions import ApplicationError


class EmailAlreadyExistsError(ApplicationError):
    """Пользователь с таким email уже существует."""  # noqa: RUF002


class InvalidCredentialsError(ApplicationError):
    """Неверная почта или пароль."""


class InvalidRefreshTokenError(ApplicationError):
    """Неверный refresh token."""


class InvalidAccessTokenError(ApplicationError):
    """Неверный access token."""
