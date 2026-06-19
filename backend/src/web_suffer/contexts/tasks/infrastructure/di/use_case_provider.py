from dishka import Provider, Scope, provide

from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.create_submission import CreateSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submission_by_id import GetSubmissionByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submissions import GetSubmissionsUseCase
from web_suffer.contexts.tasks.application.use_cases.get_task_by_id import GetTaskByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.get_tasks import GetTasksUseCase
from web_suffer.contexts.tasks.application.use_cases.get_tasks_statistics import GetTasksStatisticsUseCase
from web_suffer.contexts.tasks.application.use_cases.get_top_users import GetTopUsersUseCase
from web_suffer.contexts.tasks.application.use_cases.get_user_by_id import GetUserByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.update_task import UpdateTaskUseCase
from web_suffer.contexts.tasks.application.use_cases.update_user import UpdateUserUseCase
from web_suffer.contexts.tasks.infrastructure.mappers.task_dto_mapper import TaskDTOMapper


class TaskUseCasesProvider(Provider):
    """Провайдер для всей Task UseCase."""

    scope = Scope.REQUEST

    task_dto_mapper = provide(
        TaskDTOMapper,
        provides=ITaskDTOMapper,
        scope=Scope.APP,
    )

    change_submission = provide(ChangeSubmissionUseCase)
    create_submission = provide(CreateSubmissionUseCase)
    get_submission_by_id = provide(GetSubmissionByIDUseCase)
    get_submissions = provide(GetSubmissionsUseCase)
    get_task_by_id = provide(GetTaskByIDUseCase)
    get_tasks_statistics = provide(GetTasksStatisticsUseCase)
    get_tasks = provide(GetTasksUseCase)
    get_top_users = provide(GetTopUsersUseCase)
    get_user_by_id = provide(GetUserByIDUseCase)
    update_task = provide(UpdateTaskUseCase)
    update_user = provide(UpdateUserUseCase)
