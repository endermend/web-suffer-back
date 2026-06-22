import { defineStore } from 'pinia'
import taskService from '@/services/api/task_service.ts'
import authService from '@/services/api/auth_service.ts'

interface Notification {
  id: number
  message: string
  type?: 'accepted' | 'rejected'
}

let nextId = 0
let pollHandle: ReturnType<typeof setInterval> | null = null

const POLL_INTERVAL_MS = 20000

// Persisted per-user (not just in-memory, and not cleared on logout) so the "since
// when" cursor survives page reloads *and* logout/login cycles — a submission can
// get graded while the user is logged out entirely, and they should still see that
// the next time they log back in.
function lastCheckedKey(userId: string): string {
  return `submissions_last_checked_at:${userId}`
}

const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    toasts: [] as Notification[],
  }),

  actions: {
    push(message: string, type?: 'accepted' | 'rejected') {
      this.toasts.push({ id: nextId++, message, type })
    },

    dismiss(id: number) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },

    // No backend notifications endpoint exists, so this polls /submissions filtered
    // by `updated_after` to find submissions graded since the last check.
    startPolling() {
      if (pollHandle) return
      this.checkSubmissions()
      pollHandle = setInterval(() => {
        this.checkSubmissions()
      }, POLL_INTERVAL_MS)
    },

    stopPolling() {
      if (pollHandle) {
        clearInterval(pollHandle)
        pollHandle = null
      }
      this.toasts = []
    },

    async checkSubmissions() {
      try {
        const me = await authService.getUser()
        const key = lastCheckedKey(me.user_id)
        const lastCheckedAt = localStorage.getItem(key)
        const checkedAt = new Date().toISOString()

        // First check ever (or right after login) — just establish the cursor
        // instead of notifying about every already-graded submission in history.
        if (lastCheckedAt) {
          const [tasks, submissions] = await Promise.all([
            taskService.getTasks({ limit: 100 }),
            taskService.getSubmissions({
              userId: me.user_id,
              updatedAfter: lastCheckedAt,
              orderBy: 'updated_at',
            }),
          ])
          const titleByTaskId = new Map(tasks.map((t) => [t.task_id, t.title]))

          for (const submission of submissions) {
            const title = titleByTaskId.get(submission.task_id) ?? 'Задание'
            if (submission.status === 'accepted') this.push(`Задание ${title} принято.`, 'accepted')
            else if (submission.status === 'rejected')
              this.push(`Задание ${title} отклонено.`, 'rejected')
          }
        }

        localStorage.setItem(key, checkedAt)
      } catch {}
    },
  },
})

export { useNotificationsStore }
