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

export type UserRole = 'admin' | 'member'
