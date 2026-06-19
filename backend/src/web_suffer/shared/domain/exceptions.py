class DomainError(Exception):
    """Базовая ошибка для доменного слоя."""


class InsufficientPermissionsError(DomainError):
    """Недостаточно прав доступа."""
