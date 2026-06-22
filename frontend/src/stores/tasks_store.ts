import { defineStore } from 'pinia'
import taskService from '@/services/api/task_service.ts'
import authService from '@/services/api/auth_service.ts'
import { buildDownloadUrl } from '@/services/api/config.ts'
import type { Submission, UserTask } from '@/types/tasks.ts'

const useTasksStore = defineStore('tasks', {
  state: () => ({
    myTasks: [] as UserTask[],
    mySubmissions: [] as Submission[],
    pendingReview: [] as Submission[],
    loading: false,
  }),

  getters: {
    pendingSubmissions: (state) => state.pendingReview,

    mySubmissionForTask:
      (state) =>
      (taskId: string): Submission | undefined =>
        state.mySubmissions.find((s) => s.task_id === taskId),
  },

  actions: {
    async fetchMyTasks() {
      this.loading = true
      try {
        const apiTasks = await taskService.getTasks({ limit: 100, orderBy: 'last_submission' })
        this.myTasks = apiTasks.map((t) => ({
          id: t.task_id,
          title: t.title,
          description: t.description,
          deadline: t.deadline,
          exp: t.exp,
          money: t.money,
          status: t.status,
        }))
      } finally {
        this.loading = false
      }
    },

    async fetchMySubmissions() {
      this.loading = true
      try {
        const me = await authService.getUser()
        const apiSubmissions = await taskService.getSubmissions({ userId: me.user_id })
        this.mySubmissions = apiSubmissions.map((s) => ({
          id: s.submission_id,
          task_id: s.task_id,
          user_email: me.email,
          content: s.content,
          file: s.file ? { name: s.file, url: buildDownloadUrl(s.file) } : null,
          status: s.status,
          admin_comment: s.comment,
          submitted_at: '',
        }))
      } finally {
        this.loading = false
      }
    },

    async fetchPendingReview() {
      this.loading = true
      try {
        const apiSubmissions = await taskService.getSubmissions({ status: 'pending' })
        this.pendingReview = await Promise.all(
          apiSubmissions.map(async (s) => {
            const user = await authService.getUser(s.user_id)
            return {
              id: s.submission_id,
              task_id: s.task_id,
              user_email: user.email,
              content: s.content,
              file: s.file ? { name: s.file, url: buildDownloadUrl(s.file) } : null,
              status: s.status,
              admin_comment: s.comment,
              submitted_at: '',
            }
          }),
        )
      } finally {
        this.loading = false
      }
    },

    async saveTask(data: {
      task_id?: string
      title: string
      description: string
      deadline: string
      exp: number
      money: number
    }) {
      try {
        const { task_id } = await taskService.updateTask(data)
        const existing = this.myTasks.find((t) => t.id === task_id)
        if (existing) {
          existing.title = data.title
          existing.description = data.description
          existing.deadline = data.deadline
          existing.exp = data.exp
          existing.money = data.money
        } else {
          this.myTasks.push({
            id: task_id,
            title: data.title,
            description: data.description,
            deadline: data.deadline,
            exp: data.exp,
            money: data.money,
            status: 'available',
          })
        }
        return { success: true as const }
      } catch (error: any) {
        return { success: false as const, error: error.message }
      }
    },

    async createSubmission(taskId: string, content: string, file: File | null) {
      try {
        await taskService.createSubmission(taskId, content, file)
        const task = this.myTasks.find((t) => t.id === taskId)
        if (task) task.status = 'pending'
        return { success: true as const }
      } catch (error: any) {
        return { success: false as const, error: error.message }
      }
    },

    async acceptSubmission(submissionId: string, comment: string) {
      try {
        await taskService.changeSubmission(submissionId, 'accepted', comment)
        this.pendingReview = this.pendingReview.filter((s) => s.id !== submissionId)
        return { success: true as const }
      } catch (error: any) {
        return { success: false as const, error: error.message }
      }
    },

    async rejectSubmission(submissionId: string, comment: string) {
      try {
        await taskService.changeSubmission(submissionId, 'rejected', comment)
        this.pendingReview = this.pendingReview.filter((s) => s.id !== submissionId)
        return { success: true as const }
      } catch (error: any) {
        return { success: false as const, error: error.message }
      }
    },
  },
})

export { useTasksStore }
