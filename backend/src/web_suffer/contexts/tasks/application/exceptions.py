from web_suffer.shared.application.exceptions import ApplicationError


class InvalidTaskError(ApplicationError):
    """Задание с таким id не существует."""  # noqa: RUF002
