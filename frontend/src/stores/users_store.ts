import { defineStore } from 'pinia'
import type { UserManagement } from '@/types/users.ts'

const useUsersStore = defineStore('users', {
  state: () => ({
    // TODO: replace with API call
    // NOTE: points here are independent mock data, not derived from tasksStore.completedTasks.
    // Once the backend is the source of truth, a user's points must match the same total
    // ProfilePage.vue computes from completed tasks (currently computed client-side per user).
    users: [
      { id: 1, email: 'ivan.petrov@example.com', points: 145, role: 'member', banned: false },
      { id: 2, email: 'anna.smirnova@example.com', points: 320, role: 'member', banned: false },
      { id: 3, email: 'troll228@example.com', points: 10, role: 'member', banned: true },
      { id: 4, email: 'maria.k@example.com', points: 210, role: 'member', banned: false },
    ] as UserManagement[],
  }),

  getters: {
    sortedByPoints: (state) =>
      [...state.users]
        .filter((u) => u.role === 'member')
        .sort((a, b) => b.points - a.points),
  },

  actions: {
    // TODO: replace with API call
    toggleBan(id: number) {
      const user = this.users.find((u) => u.id === id)
      if (user) user.banned = !user.banned
    },

    // TODO: replace with API call
    updateEmail(id: number, email: string) {
      const user = this.users.find((u) => u.id === id)
      if (user) user.email = email
    },

    // TODO: replace with API call
    deleteUser(id: number) {
      this.users = this.users.filter((u) => u.id !== id)
    },
  },
})

export { useUsersStore }
