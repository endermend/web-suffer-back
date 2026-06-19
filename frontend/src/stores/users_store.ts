import { defineStore } from 'pinia'
import authService from '@/services/api/auth_service.ts'
import type { UserManagement } from '@/types/users.ts'
import type { UserRole } from '@/types/auth.ts'

const useUsersStore = defineStore('users', {
  state: () => ({
    users: [] as UserManagement[],
    loading: false,
  }),

  getters: {
    sortedByPoints: (state) =>
      [...state.users]
        .filter((u) => u.role === 'member')
        .sort((a, b) => b.points - a.points),
  },

  actions: {
    // GET /api/auth/users only returns { email } for now — role/points/banned have no
    // backing endpoint yet, so existing local state for a known email is preserved across
    // refetches. `id` is synthesized from list position until the backend adds a real one.
    async fetchUsers() {
      this.loading = true

      try {
        const apiUsers = await authService.getUsers()
        this.users = apiUsers.map((apiUser, index) => {
          const existing = this.users.find((u) => u.email === apiUser.email)
          return (
            existing ?? {
              id: index + 1,
              email: apiUser.email,
              points: 0,
              role: 'member',
              banned: false,
            }
          )
        })
      } finally {
        this.loading = false
      }
    },

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
    setUserRole(id: number, role: UserRole) {
      const user = this.users.find((u) => u.id === id)
      if (user) user.role = role
    },

    // TODO: replace with API call
    deleteUser(id: number) {
      this.users = this.users.filter((u) => u.id !== id)
    },
  },
})

export { useUsersStore }
