import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Form, Query, UploadFile, status

from web_suffer.contexts.tasks.application.dtos.submission_dto import (
    ChangeSubmissionDTO,
    CreateSubmissionDTO,
    SubmissionRangesDTO,
    SubmissionTokenIDDTO,
)
from web_suffer.contexts.tasks.application.dtos.task_dto import TaskIDDTO, UpdateTaskDTO, UsersTasksRangeDTO
from web_suffer.contexts.tasks.application.dtos.usert_dto import UpdateUserTDTO, UserTIDDTO
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.create_submission import CreateSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submission_by_id import GetSubmissionByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submissions import GetSubmissionsUseCase
from web_suffer.contexts.tasks.application.use_cases.get_task_by_id import GetTaskByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.get_tasks import GetTasksUseCase
from web_suffer.contexts.tasks.application.use_cases.get_tasks_statistics import GetTasksStatisticsUseCase
from web_suffer.contexts.tasks.application.use_cases.get_user_by_id import GetUserByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.update_task import UpdateTaskUseCase
from web_suffer.contexts.tasks.application.use_cases.update_user import UpdateUserUseCase
from web_suffer.contexts.tasks.domain.types import SubmissionOrderBy, SubmissionStatus, TaskOrderBy, TaskStatusFilter
from web_suffer.infrastructure.constants import UPLOAD_DIR
from web_suffer.presentation.api.routers.utils import CredentialsType, OptionalCredentialsType
from web_suffer.presentation.api.schemas.task.change_submission import ChangeSubmissionRequest
from web_suffer.presentation.api.schemas.task.submission import SubmissionResponce
from web_suffer.presentation.api.schemas.task.task import TaskResponce
from web_suffer.presentation.api.schemas.task.tasks import UserTaskResponce
from web_suffer.presentation.api.schemas.task.tasks_statistics import TaskStatisticsResponce
from web_suffer.presentation.api.schemas.task.update_task import UpdateTaskRequest, UpdateTaskResponse
from web_suffer.presentation.api.schemas.task.update_user import UpdateUserRequest
from web_suffer.presentation.api.schemas.task.user import UserResponce
from web_suffer.shared.application.dtos.access_token_dto import PublicAccessTokenDTO

router = APIRouter(prefix="/task", tags=["Task"])


@router.post(
    "/change-submission",
    status_code=status.HTTP_200_OK,
    summary="Проверка отправления",
)
@inject
async def change_submission(
    credentials: CredentialsType,
    data: ChangeSubmissionRequest,
    use_case: FromDishka[ChangeSubmissionUseCase],
) -> None:
    """Эндпоинт проверки отправления."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=ChangeSubmissionDTO(
            access_token=access_token,
            submission_id=data.submission_id,
            status=data.status,
            comment=data.comment or "",
        ),
    )


@router.post(
    "/create-submission",
    status_code=status.HTTP_200_OK,
    summary="Создание отправления",
)
@inject
async def create_submission(
    credentials: CredentialsType,
    task_id: Annotated[uuid.UUID, Form()],
    content: Annotated[str, Form()],
    use_case: FromDishka[CreateSubmissionUseCase],
    file: Annotated[UploadFile | None, File()] = None,
) -> None:
    """Эндпоинт создания отправления."""
    access_token = credentials.credentials
    file_path: Path | None = None
    if file is not None:
        file_name = uuid.uuid4()
        file_path = UPLOAD_DIR / f"{file_name}{Path(file.filename).suffix if file.filename is not None else ''}"

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    await use_case.execute(
        input_dto=CreateSubmissionDTO(
            access_token=access_token,
            task_id=task_id,
            content=content,
            file=file_path,
        ),
    )


@router.post(
    "/update-task",
    status_code=status.HTTP_200_OK,
    summary="Создание/изменение заданий",
)
@inject
async def update_task(
    credentials: CredentialsType,
    data: UpdateTaskRequest,
    use_case: FromDishka[UpdateTaskUseCase],
) -> UpdateTaskResponse:
    """
    Эндпоинт создания задания.

    Returns:
        ID нового/измененного задания.

    """
    access_token = credentials.credentials
    task_id = await use_case.execute(
        input_dto=UpdateTaskDTO(
            access_token=access_token,
            task_id=data.task_id,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            exp=data.exp,
            money=data.money,
        ),
    )
    return UpdateTaskResponse(
        task_id=task_id.task_id,
    )


@router.post(
    "/update-user",
    status_code=status.HTTP_200_OK,
    summary="Изменение пользователя.",
)
@inject
async def update_user(
    credentials: CredentialsType,
    data: UpdateUserRequest,
    use_case: FromDishka[UpdateUserUseCase],
) -> None:
    """Эндпоинт изменения пользователя."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=UpdateUserTDTO(
            access_token=access_token,
            user_id=data.user_id,
            exp_diff=data.exp_diff,
            money_diff=data.money_diff,
        ),
    )


@router.get(
    "/submission",
    status_code=status.HTTP_200_OK,
    summary="Получение отправления",
)
@inject
async def submission(
    credentials: CredentialsType,
    submission_id: Annotated[uuid.UUID, Query(description="ID отправления")],
    use_case: FromDishka[GetSubmissionByIDUseCase],
) -> SubmissionResponce:
    """
    Эндпоинт получения отправления.

    Returns:
        SubmissionResponce

    """
    access_token = credentials.credentials
    output_dto = await use_case.execute(
        input_dto=SubmissionTokenIDDTO(
            access_token=access_token,
            submission_id=submission_id,
        ),
    )
    return SubmissionResponce(
        submission_id=output_dto.submission_id,
        task_id=output_dto.task_id,
        user_id=output_dto.user_id,
        content=output_dto.content,
        file=output_dto.file.name if output_dto.file is not None else None,
        status=output_dto.status,
        comment=output_dto.comment,
    )


@router.get(
    "/submissions",
    status_code=status.HTTP_200_OK,
    summary="Получение отправлений по фильтру",
)
@inject
async def submissions(
    credentials: CredentialsType,
    use_case: FromDishka[GetSubmissionsUseCase],
    user_id: Annotated[uuid.UUID | None, Query(description="ID отправителя")] = None,
    status: Annotated[SubmissionStatus | None, Query(description="Статус отправления")] = None,
    order_by: Annotated[SubmissionOrderBy | None, Query(description="Призрак сортировки")] = None,
) -> list[SubmissionResponce]:
    """
    Эндпоинт получения отправлений по фильтру.

    Returns:
        Список отправлений.

    """
    access_token = credentials.credentials
    subms = await use_case.execute(
        input_dto=SubmissionRangesDTO(
            access_token=access_token,
            user_id=user_id,
            status=status,
            order_by=order_by,
        ),
    )
    return [
        SubmissionResponce(
            submission_id=subm.submission_id,
            task_id=subm.task_id,
            user_id=subm.user_id,
            content=subm.content,
            file=subm.file.name if subm.file is not None else None,
            status=subm.status,
            comment=subm.comment,
        )
        for subm in subms
    ]


@router.get(
    "/task",
    status_code=status.HTTP_200_OK,
    summary="Получение задания",
)
@inject
async def task(
    task_id: Annotated[uuid.UUID, Query(description="ID задания")],
    use_case: FromDishka[GetTaskByIDUseCase],
) -> TaskResponce:
    """
    Эндпоинт получения описания задания.

    Returns:
        TaskResponce

    """
    output_dto = await use_case.execute(
        input_dto=TaskIDDTO(
            task_id=task_id,
        ),
    )
    return TaskResponce(
        task_id=output_dto.task_id,
        title=output_dto.title,
        description=output_dto.description,
        deadline=output_dto.deadline,
        exp=output_dto.exp,
        money=output_dto.money,
    )


@router.get(
    "/tasks-statistics",
    status_code=status.HTTP_200_OK,
    summary="Получение статистики о заданиях",
)
@inject
async def tasks_statistics(
    use_case: FromDishka[GetTasksStatisticsUseCase],
    credentials: OptionalCredentialsType = None,
) -> TaskStatisticsResponce:
    """
    Эндпоинт получения статистики о заданиях.

    Если access_token не указан, возвращает только общее число доступных задач.

    Returns:
        TaskStatisticsResponce

    """  # noqa: RUF002
    access_token = credentials.credentials if credentials is not None else None
    output_dto = await use_case.execute(
        input_dto=PublicAccessTokenDTO(
            access_token=access_token,
        ),
    )
    return TaskStatisticsResponce(
        task_all=output_dto.tasks_all,
        task_status=output_dto.tasks_status,
    )


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    summary="Получение заданий пользователя по фильтру",
)
@inject
async def tasks(
    credentials: CredentialsType,
    use_case: FromDishka[GetTasksUseCase],
    limit: Annotated[int, Query(description="Предел записей", le=100, ge=1)] = 20,
    offset: Annotated[int, Query(description="Отступ от начала")] = 0,
    deadline_from: Annotated[datetime | None, Query(description="Дедлайн от")] = None,
    deadline_till: Annotated[datetime | None, Query(description="Дедлайн до")] = None,
    status: Annotated[TaskStatusFilter | None, Query(description="Статус задания")] = None,
    order_by: Annotated[TaskOrderBy | None, Query(description="Порядок сортировки")] = None,
) -> list[UserTaskResponce]:
    """
    Эндпоинт получения списка заданий.

    Returns:
        list[UserTaskResponce]

    """
    access_token = credentials.credentials if credentials is not None else None
    tasks = await use_case.execute(
        input_dto=UsersTasksRangeDTO(
            access_token=access_token,
            deadline_from=deadline_from,
            deadline_till=deadline_till,
            status=status,
            order_by=order_by,
            limit=limit,
            offset=offset,
        ),
    )
    return [
        UserTaskResponce(
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            exp=task.exp,
            money=task.money,
            status=task.status,
        )
        for task in tasks
    ]


@router.get(
    "/user",
    status_code=status.HTTP_200_OK,
    summary="Получение информации о пользователе по ID.",
)
@inject
async def user(
    credentials: CredentialsType,
    use_case: FromDishka[GetUserByIDUseCase],
    user_id: Annotated[uuid.UUID | None, Query(description="ID пользователя")] = None,
) -> UserResponce:
    """
    Эндпоинт получения информации о пользователе.

    Если ID не указан, возвращает информацию о пользователе по access_token.

    Returns:
        UserResponce

    """  # noqa: RUF002
    access_token = credentials.credentials if credentials is not None else None
    user = await use_case.execute(
        input_dto=UserTIDDTO(
            access_token=access_token,
            user_id=user_id,
        ),
    )
    return UserResponce(
        user_id=user.user_id,
        exp=user.exp,
        money=user.money,
    )
