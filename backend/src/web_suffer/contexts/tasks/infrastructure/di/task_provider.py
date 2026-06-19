from dishka import Provider

from web_suffer.contexts.tasks.infrastructure.di.db_provider import TaskDBProvider
from web_suffer.contexts.tasks.infrastructure.di.use_case_provider import TaskUseCasesProvider


class TaskProvider(
    TaskDBProvider,
    TaskUseCasesProvider,
    Provider,
):
    """Провайдер, объединяющий провайдеры заданий."""
