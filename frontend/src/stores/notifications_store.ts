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
let myUserId: string | null = null
let prevSubmissions: Map<string, { status: string; taskId: string }> | null = null
let prevRank: number | null = null
let prevAboveUserId: string | null = null

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
      myUserId = null
      prevSubmissions = null
      prevRank = null
      prevAboveUserId = null
    },

    async checkSubmissions() {
      try {
        const me = await authService.getUser()
        myUserId = me.user_id
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
        if (!myUserId) {
          const me = await authService.getUser()
          myUserId = me.user_id
        }
        const topUsers = await taskService.getTopUsers(9999)
        const sorted = [...topUsers].sort((a, b) => b.exp - a.exp)
        const myIndex = sorted.findIndex((u) => u.user_id === myUserId)
        if (myIndex === -1) return

        const aboveUserId = myIndex > 0 ? (sorted[myIndex - 1]?.user_id ?? null) : null

        if (prevRank !== null && myIndex < prevRank && prevAboveUserId) {
          const overtaken = await authService.getUser(prevAboveUserId)
          this.push(`Вы обогнали пользователя ${overtaken.email}.`)
        }

        prevRank = myIndex
        prevAboveUserId = aboveUserId
      } catch {
        // same as above — best-effort, retried on the next tick
      }
    },
  },
})

export { useNotificationsStore }
