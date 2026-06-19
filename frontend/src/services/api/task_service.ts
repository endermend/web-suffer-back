import axios from 'axios'
import type {
  ChangeSubmissionRequest,
  SubmissionStatus,
  UpdateTaskRequest,
  UpdateTaskResponse,
  UpdateUserExpRequest,
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

class TaskService {
  // creates a task when task_id is omitted, edits it otherwise
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

  // response body is empty per the spec — only the status code tells us it worked
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
}

export default new TaskService()
