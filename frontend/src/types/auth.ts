export interface AuthCredentials {
  email: string
  password: string
}

export interface AuthToken {
  access_token: string
}

export interface EmailResponse {
  email: string
}

export interface GetUsersResponse {
  user_id: string
}

export type UserRole = 'admin' | 'moderator' | 'member'
export type ApiUserRole = 'user' | 'admin' | 'moderator'
export type ApiUserStatus = 'active' | 'banned' | 'deleted'

export interface UpdateUserParams {
  user_id?: string
  email?: string
  role?: ApiUserRole
  status?: ApiUserStatus
  new_password?: string
}

export interface UserResponse {
  user_id: string
  email: string
  role: ApiUserRole
  status: ApiUserStatus
}
