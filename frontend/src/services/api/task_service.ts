import axios from 'axios'
import authService from '@/services/api/auth_service.ts'
import { isExpiredAccessTokenError } from '@/services/api/token_error.ts'
import type {
  ChangeSubmissionRequest,
  GetTasksFilters,
  SubmissionApiResponse,
  SubmissionOrderBy,
  SubmissionStatus,
  TaskApiResponse,
  TaskStatisticsResponse,
  TopUserApiResponse,
  UpdateTaskRequest,
  UpdateTaskResponse,
  UpdateUserExpRequest,
  UserTaskApiResponse,
} from '@/types/tasks.ts'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

// same bearer wiring as auth_service's apiClient — each axios instance needs its own
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// authService.refresh() shares its in-flight promise with auth_service's own interceptor,
// so an expired-token error here and one over there at the same time still only refresh once.
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config

    if (isExpiredAccessTokenError(error) && !config._retry) {
      config._retry = true
      try {
        const { access_token } = await authService.refresh()
        config.headers.Authorization = `Bearer ${access_token}`
        return apiClient(config)
      } catch {
        const { useAuthStore } = await import('@/stores/auth_store.ts')
        useAuthStore().logout()
      }
    }

    return Promise.reject(error)
  },
)

class TaskService {
  async updateTask(data: UpdateTaskRequest): Promise<UpdateTaskResponse> {
    try {
      const response = await apiClient.post<UpdateTaskResponse>('/api/task/update-task', data)
      return response.data
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Недостаточно прав для управления заданиями')
          case 422:
            throw new Error('Неверные данные задания')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async createSubmission(taskId: string, content: string, file: File | null): Promise<void> {
    try {
      const formData = new FormData()
      formData.append('task_id', taskId)
      formData.append('content', content)
      if (file) formData.append('file', file)

      await apiClient.post('/api/task/create-submission', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Недостаточно прав для отправки ответа')
          case 422:
            throw new Error('Неверные данные ответа')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async changeSubmission(
    submissionId: string,
    status: SubmissionStatus,
    comment?: string,
  ): Promise<void> {
    try {
      const payload: ChangeSubmissionRequest = { submission_id: submissionId, status, comment }
      await apiClient.post('/api/task/change-submission', payload)
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Недостаточно прав для проверки задания')
          case 422:
            throw new Error('Неверные данные проверки')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async updateUserExp(userId: string, expDiff: number, moneyDiff: number): Promise<void> {
    try {
      const payload: UpdateUserExpRequest = {
        user_id: userId,
        exp_diff: expDiff,
        money_diff: moneyDiff,
      }
      await apiClient.post('/api/task/update-user', payload)
    } catch (error: any) {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            throw new Error('Недостаточно прав для начисления баллов')
          case 422:
            throw new Error('Неверные данные начисления')
        }
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getTask(taskId: string): Promise<TaskApiResponse> {
    try {
      const response = await apiClient.get<TaskApiResponse>('/api/task/task', {
        params: { task_id: taskId },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить задание')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getSubmission(submissionId: string): Promise<SubmissionApiResponse> {
    try {
      const response = await apiClient.get<SubmissionApiResponse>('/api/task/submission', {
        params: { submission_id: submissionId },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить сдачу')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getSubmissions(filters?: {
    userId?: string
    status?: SubmissionStatus
    updatedAfter?: string
    orderBy?: SubmissionOrderBy
  }): Promise<SubmissionApiResponse[]> {
    try {
      const response = await apiClient.get<SubmissionApiResponse[]>('/api/task/submissions', {
        params: {
          user_id: filters?.userId,
          status: filters?.status,
          updated_after: filters?.updatedAfter,
          order_by: filters?.orderBy,
        },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить список сдач')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getTasksStatistics(): Promise<TaskStatisticsResponse> {
    try {
      const response = await apiClient.get<TaskStatisticsResponse>('/api/task/tasks-statistics')
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить статистику заданий')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  // per-user task list
  async getTasks(filters?: GetTasksFilters): Promise<UserTaskApiResponse[]> {
    try {
      const response = await apiClient.get<UserTaskApiResponse[]>('/api/task/tasks', {
        params: {
          limit: filters?.limit,
          offset: filters?.offset,
          deadline_from: filters?.deadlineFrom,
          deadline_till: filters?.deadlineTill,
          status: filters?.status,
          order_by: filters?.orderBy,
        },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить список заданий')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }

  async getTopUsers(limit?: number): Promise<TopUserApiResponse[]> {
    try {
      const response = await apiClient.get<TopUserApiResponse[]>('/api/task/top-users', {
        params: { limit },
      })
      return response.data
    } catch (error: any) {
      if (error.response) {
        throw new Error('Не удалось получить таблицу лидеров')
      }
      throw new Error('Ошибка соединения с сервером')
    }
  }
}

export default new TaskService()
