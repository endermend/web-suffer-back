from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


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
