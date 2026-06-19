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

// POST /api/auth/update-user — query params, all optional. Omitting user_id targets self.
// `status` is an int enum on the backend; exact values aren't known yet.
export interface UpdateUserParams {
  user_id?: string
  email?: string
  role?: string
  status?: number
  new_password?: string
}
