import axios from 'axios'
import type { AuthCredentials, AuthToken, EmailResponse } from '@/types/auth.ts'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

class AuthService {
  // register
  async register({ email, password }: AuthCredentials): Promise<AuthToken> {
    try {
      const credentials: AuthCredentials = { email, password }
      const response = await apiClient.post<AuthToken>('api/auth/register', credentials)

      return response.data
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 409:
            throw new Error('Пользователь с таким email уже существует')
          case 422:
            throw new Error('Неверный формат логина или пароля')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  // login
  async login({ email, password }: AuthCredentials): Promise<AuthToken> {
    try {
      const credentials: AuthCredentials = { email, password }
      const response = await apiClient.post<AuthToken>('api/auth/login', credentials)

      return response.data
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Неверный логин или пароль')
          case 422:
            throw new Error('Неверный формат логина или пароля')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async refresh(): Promise<AuthToken> {
    const response = await apiClient.post<AuthToken>('/api/auth/refresh')
    return response.data
  }

  async getEmail(): Promise<EmailResponse> {
    try {
      const token = localStorage.getItem('access_token')
      const response = await apiClient.get<EmailResponse>('/api/auth/email', {
        params: {
          access_token: token,
        },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error(error.response.data)
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }
}

export default new AuthService()
