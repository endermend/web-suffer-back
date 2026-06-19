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

// GET /api/auth/users — backend only returns email for now, an id is planned later
export interface GetUsersResponse {
  email: string
}

export type UserRole = 'admin' | 'moderator' | 'member'

// Backend's own role/status literals — distinct from the frontend's UserRole
// ('user' not 'member') since UserRole also drives the local dev role-switcher.
export type ApiUserRole = 'user' | 'admin' | 'moderator'
export type ApiUserStatus = 'active' | 'banned' | 'deleted'

// POST /api/auth/update-user — query params, all optional. Omitting user_id targets self.
export interface UpdateUserParams {
  user_id?: string
  email?: string
  role?: ApiUserRole
  status?: ApiUserStatus
  new_password?: string
}

// GET /api/auth/user — omitting user_id returns the current user's own data
export interface UserResponse {
  user_id: string
  email: string
  role: ApiUserRole
  status: ApiUserStatus
}
