export interface SubmissionFile {
  name: string
  url: string
}

// Task is the reusable template an admin creates. No per-user state lives here —
// mirrors the backend's Task entity/TaskDTO (title, description, deadline, exp, money).
// `money` exists on the type to match the backend shape but isn't shown in the UI yet —
// `exp` is what our old `points` field maps to and is the only reward we display.
export interface Task {
  id: string
  title: string
  description: string
  deadline: string
  exp: number
  money: number
}

// Status names match the backend's SubmissionStatus/TaskStatus literals exactly,
// so there's no translation layer to maintain once this talks to the real API.
export type SubmissionStatus = 'pending' | 'accepted' | 'rejected'
export type UserTaskStatus = 'available' | SubmissionStatus

// Submission is one attempt by one user at one task. Resubmitting after a rejection
// creates a NEW row instead of mutating the old one — the backend keeps every attempt
// and resolves the "current" status by priority (accepted > pending > rejected).
export interface Submission {
  id: string
  task_id: string
  user_email: string
  content: string
  file: SubmissionFile | null
  status: SubmissionStatus
  admin_comment: string
  submitted_at: string
}

// Per-user view of a task (Task + derived status) — equivalent to the backend's
// UsersTaskDTO. Always computed by joining tasks with the user's submissions,
// never stored directly.
export interface UserTask extends Task {
  status: UserTaskStatus
}

// POST /api/task/update_task — task_id omitted/null creates a new task.
export interface UpdateTaskRequest {
  task_id?: string | null
  title: string
  description: string
  deadline: string
  exp: number
  money: number
}

export interface UpdateTaskResponse {
  task_id: string
}

// POST /api/task/change_submission
export interface ChangeSubmissionRequest {
  submission_id: string
  status: SubmissionStatus
  comment?: string | null
}

// POST /api/task/update_user — awards exp/money to a user, e.g. on accepting a submission.
export interface UpdateUserExpRequest {
  user_id: string
  exp_diff: number
  money_diff: number
}

// GET /api/task/task
export interface TaskApiResponse {
  task_id: string
  title: string
  description: string
  deadline: string
  exp: number
  money: number
}

// GET /api/task/submission, GET /api/task/submissions
export interface SubmissionApiResponse {
  submission_id: string
  task_id: string
  user_id: string
  content: string
  file: string | null
  status: SubmissionStatus
  comment: string
}

export type SubmissionOrderBy = 'status' | 'created_at' | 'task_title'

// GET /api/task/tasks-statistics
export interface TaskStatisticsResponse {
  task_all: number
  task_status: Partial<Record<UserTaskStatus, number>> | null
}
