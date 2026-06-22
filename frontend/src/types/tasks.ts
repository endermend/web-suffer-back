export interface SubmissionFile {
  name: string
  url: string
}

export interface Task {
  id: string
  title: string
  description: string
  deadline: string
  exp: number
  money: number
}

export type SubmissionStatus = 'pending' | 'accepted' | 'rejected'
export type UserTaskStatus = 'available' | SubmissionStatus

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

// Per-user view of a task
export interface UserTask extends Task {
  status: UserTaskStatus
}

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

export interface ChangeSubmissionRequest {
  submission_id: string
  status: SubmissionStatus
  comment?: string | null
}

export interface UpdateUserExpRequest {
  user_id: string
  exp_diff: number
  money_diff: number
}

export interface TaskApiResponse {
  task_id: string
  title: string
  description: string
  deadline: string
  exp: number
  money: number
}

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

export interface TaskStatisticsResponse {
  task_all: number
  task_status: Partial<Record<UserTaskStatus, number>> | null
}

export type TaskStatusFilter = 'available' | 'pending' | 'accepted'
export type TaskOrderBy = 'title' | 'deadline' | 'status' | 'last_submission'

export interface GetTasksFilters {
  limit?: number
  offset?: number
  deadlineFrom?: string
  deadlineTill?: string
  status?: TaskStatusFilter
  orderBy?: TaskOrderBy
}

export interface UserTaskApiResponse {
  task_id: string
  title: string
  description: string
  deadline: string
  exp: number
  money: number
  status: UserTaskStatus
}

export interface TopUserApiResponse {
  user_email: string
  exp: number
  money: number
}
