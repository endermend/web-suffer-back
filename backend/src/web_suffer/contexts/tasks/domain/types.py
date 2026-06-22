from typing import Literal

type TaskStatus = Literal["available", "pending", "accepted", "rejected"]
type TaskStatusFilter = Literal["available", "pending", "accepted"]
type TaskOrderBy = Literal["title", "deadline", "status", "last_submission"]

type SubmissionStatus = Literal["pending", "accepted", "rejected"]
type SubmissionOrderBy = Literal["status", "created_at", "task_title", "updated_at"]
