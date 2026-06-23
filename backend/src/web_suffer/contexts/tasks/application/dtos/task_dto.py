from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from web_suffer.contexts.tasks.domain.types import TaskOrderByType, TaskStatusFilterType, TaskStatusType


@dataclass(slots=True, frozen=True)
class TaskDTO:
    """DTO задания."""

    task_id: UUID
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int


@dataclass(slots=True, frozen=True)
class TaskIDDTO:
    """DTO ID задания."""

    task_id: UUID


@dataclass(slots=True, frozen=True)
class UsersTasksRangeDTO:
    """DTO фильтра заданий пользователя."""

    access_token: str
    deadline_from: datetime | None
    deadline_till: datetime | None
    status: TaskStatusFilterType | None
    order_by: TaskOrderByType | None
    limit: int
    offset: int


@dataclass(slots=True, frozen=True)
class UsersTaskDTO:
    """DTO задания пользователя."""

    task_id: UUID
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
    status: TaskStatusType


@dataclass(slots=True, frozen=True)
class TaskStatisticsDTO:
    """DTO статистики заданий."""

    tasks_all: int

    tasks_status: dict[TaskStatusType, int] | None


@dataclass(slots=True, frozen=True)
class UpdateTaskDTO:
    """DTO создания/изменения задания."""

    access_token: str
    task_id: UUID | None
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
