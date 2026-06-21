import { defineStore } from 'pinia'
import taskService from '@/services/api/task_service.ts'
import authService from '@/services/api/auth_service.ts'

interface Notification {
  id: number
  message: string
}

let nextId = 0
let pollHandle: ReturnType<typeof setInterval> | null = null

// Diff snapshots from the previous poll. Kept as module-level state rather than
// store state since nothing in the UI reads them — only the notifications they produce.
let myEmail: string | null = null
let prevSubmissions: Map<string, { status: string; taskId: string }> | null = null
let prevRank: number | null = null
let prevAboveEmail: string | null = null

const POLL_INTERVAL_MS = 20000

const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    toasts: [] as Notification[],
  }),

  actions: {
    push(message: string) {
      this.toasts.push({ id: nextId++, message })
    },

    dismiss(id: number) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },

    // No backend notifications endpoint exists, so this polls the existing
    // submissions/leaderboard endpoints and diffs each snapshot against the
    // previous poll to synthesize "submission graded" / "overtaken" events.
    startPolling() {
      if (pollHandle) return
      this.checkSubmissions()
      this.checkLeaderboard()
      pollHandle = setInterval(() => {
        this.checkSubmissions()
        this.checkLeaderboard()
      }, POLL_INTERVAL_MS)
    },

    stopPolling() {
      if (pollHandle) {
        clearInterval(pollHandle)
        pollHandle = null
      }
      myEmail = null
      prevSubmissions = null
      prevRank = null
      prevAboveEmail = null
    },

    async checkSubmissions() {
      try {
        const me = await authService.getUser()
        const [tasks, submissions] = await Promise.all([
          taskService.getTasks({ limit: 100 }),
          taskService.getSubmissions({ userId: me.user_id }),
        ])
        const titleByTaskId = new Map(tasks.map((t) => [t.task_id, t.title]))
        const current = new Map(
          submissions.map((s) => [s.submission_id, { status: s.status, taskId: s.task_id }]),
        )

        if (prevSubmissions) {
          for (const [id, { status, taskId }] of current) {
            const prev = prevSubmissions.get(id)
            if (prev?.status === 'pending' && status !== 'pending') {
              const title = titleByTaskId.get(taskId) ?? 'Задание'
              if (status === 'accepted') this.push(`Задание ${title} принято.`)
              else if (status === 'rejected') this.push(`Задание ${title} отклонено.`)
            }
          }
        }
        prevSubmissions = current
      } catch {
        // best-effort background polling — a failed check just waits for the next tick
      }
    },

    async checkLeaderboard() {
      try {
        if (!myEmail) {
          const me = await authService.getUser()
          myEmail = me.email
        }
        // /api/task/top-users now returns the email directly, so no per-row lookup is needed
        const topUsers = await taskService.getTopUsers(20)
        const sorted = [...topUsers].sort((a, b) => b.exp - a.exp)
        const myIndex = sorted.findIndex((u) => u.user_email === myEmail)
        if (myIndex === -1) return

        const aboveEmail = myIndex > 0 ? (sorted[myIndex - 1]?.user_email ?? null) : null

        if (prevRank !== null && myIndex < prevRank && prevAboveEmail) {
          this.push(`Вы обогнали пользователя ${prevAboveEmail}.`)
        }

        prevRank = myIndex
        prevAboveEmail = aboveEmail
      } catch {
        // same as above — best-effort, retried on the next tick
      }
    },
  },
})

export { useNotificationsStore }
