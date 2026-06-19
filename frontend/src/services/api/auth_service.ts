import axios from 'axios'
import type {
  AuthCredentials,
  AuthToken,
  EmailResponse,
  GetUsersResponse,
  UpdateUserParams,
  UserResponse,
} from '@/types/auth.ts'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

// bearer
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// refresh and access token management
let refreshPromise: Promise<string> | null = null

function refreshAccessToken(): Promise<string> {
  if (!refreshPromise) {
    refreshPromise = apiClient
      .post<AuthToken>('/api/auth/refresh')
      .then((response) => {
        localStorage.setItem('access_token', response.data.access_token)
        return response.data.access_token
      })
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

// refresh token failed - then log out
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config
    const isRefreshCall = config?.url?.includes('auth/refresh')

    if (error.response?.status === 401 && !isRefreshCall && !config._retry) {
      config._retry = true
      try {
        const token = await refreshAccessToken()
        config.headers.Authorization = `Bearer ${token}`
        return apiClient(config)
      } catch {
        const { useAuthStore } = await import('@/stores/auth_store.ts')
        useAuthStore().logout()
      }
    }

    return Promise.reject(error)
  },
)

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

  // Goes through the same dedup as the response interceptor — calling this directly
  // while a 401-triggered refresh is already in flight reuses that one request.
  async refresh(): Promise<AuthToken> {
    const access_token = await refreshAccessToken()
    return { access_token }
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

  // omitting user_id returns the currently authenticated user's own data (incl. their id)
  async getUser(userId?: string): Promise<UserResponse> {
    try {
      const response = await apiClient.get<UserResponse>('/api/auth/user', {
        params: userId ? { user_id: userId } : undefined,
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить данные пользователя')
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
