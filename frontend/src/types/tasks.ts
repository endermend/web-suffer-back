export interface SubmissionFile {
  name: string
  url: string
}

// Task is the reusable template an admin creates. No per-user state lives here —
// mirrors the backend's Task entity/TaskDTO (title, description, deadline, exp, money).
// `money` exists on the type to match the backend shape but isn't shown in the UI yet —
// `exp` is what our old `points` field maps to and is the only reward we display.
export interface Task {
  id: number
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
  id: number
  task_id: number
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
