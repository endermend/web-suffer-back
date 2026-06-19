from web_suffer.shared.application.exceptions import ApplicationError


class UnauthorizedCallError(ApplicationError):
    """Нет access токена."""
