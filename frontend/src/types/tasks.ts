export interface SubmissionFile {
  id: number
  name: string
  url: string
}

export interface Task {
  id: number
  title: string
  description: string
  deadline: string
  points: number
  answer: string
  submission_files: SubmissionFile[]
  status: 'available' | 'submitted' | 'graded' | 'rejected'
  submitted_at?: string
  submitted_by?: string
  admin_comment?: string
}
