import type { UserRole } from '@/types/auth.ts'

export interface User {
  id: number
  email: string
  points: number
  role: UserRole
}

export interface UserManagement extends User {
  banned: boolean
}
