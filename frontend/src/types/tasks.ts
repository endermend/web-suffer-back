export interface Task {
  id: number
  title: string
  description: string
  deadline: string
  points: number
  answer: string
  status: 'available' | 'submitted' | 'graded'
  submitted_at?: string
}
