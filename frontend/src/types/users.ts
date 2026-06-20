import type { ApiUserRole, ApiUserStatus } from '@/types/auth.ts'

export interface User {
  id: string
  email: string
  role: ApiUserRole
}

export interface UserManagement extends User {
  status: ApiUserStatus
}
