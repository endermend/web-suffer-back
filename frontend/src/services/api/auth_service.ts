import axios from 'axios'
import type {
  AuthCredentials,
  AuthToken,
  EmailResponse,
  GetUsersResponse,
  UpdateUserParams,
} from '@/types/auth.ts'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

// axios instances don't inherit headers set on the global axios.defaults object, so the
// bearer has to be attached here, read straight from localStorage on every request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
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
      const response = await apiClient.get<EmailResponse>('/api/auth/email')
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error(error.response.data)
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getUsers(): Promise<GetUsersResponse[]> {
    try {
      const response = await apiClient.get<GetUsersResponse[]>('/api/auth/users')
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить список пользователей')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  // omitting user_id targets the currently authenticated user
  async updateUser(params: UpdateUserParams): Promise<void> {
    try {
      await apiClient.post('/api/auth/update-user', null, { params })
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Недостаточно прав для изменения пользователя')
          case 422:
            throw new Error('Неверные данные')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }
}

export default new AuthService()
