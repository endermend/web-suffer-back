from typing import Literal

type TaskStatus = Literal["available", "pending", "accepted", "rejected"]
type TaskStatusFilter = Literal["available", "pending", "accepted"]
type TaskOrderBy = Literal["title", "deadline", "status", "last_submission"]
