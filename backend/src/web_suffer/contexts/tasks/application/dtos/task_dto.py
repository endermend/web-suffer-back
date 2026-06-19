from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from web_suffer.contexts.tasks.domain.types import TaskOrderBy, TaskStatus, TaskStatusFilter


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
    status: TaskStatusFilter | None
    order_by: TaskOrderBy | None
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
    status: TaskStatus


@dataclass(slots=True, frozen=True)
class TaskStatisticsDTO:
    """DTO статистики заданий."""

    tasks_all: int

    tasks_status: dict[TaskStatus, int] | None


class CreateTaskDTO:
    """DTO создания задания."""

    access_token: str
    task_id: UUID | None
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
