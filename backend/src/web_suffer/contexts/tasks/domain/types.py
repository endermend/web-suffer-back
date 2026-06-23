from typing import Literal

type TaskStatusType = Literal["available", "pending", "accepted", "rejected"]
type TaskStatusFilterType = Literal["available", "pending", "accepted"]
type TaskOrderByType = Literal["title", "deadline", "status", "last_submission"]

type SubmissionStatusType = Literal["pending", "accepted", "rejected"]
type SubmissionOrderByType = Literal["status", "created_at", "task_title", "updated_at"]
