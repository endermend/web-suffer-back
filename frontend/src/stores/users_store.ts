import { defineStore } from 'pinia'
import authService from '@/services/api/auth_service.ts'
import type { ApiUserRole, ApiUserStatus } from '@/types/auth.ts'
import type { UserManagement } from '@/types/users.ts'

const useUsersStore = defineStore('users', {
  state: () => ({
    users: [] as UserManagement[],
    loading: false,
  }),

  actions: {
    // GET /api/auth/users only returns ids — full profile (email/role/status) per id
    // comes from GET /api/auth/user.
    async fetchUsers() {
      this.loading = true

      try {
        const ids = await authService.getUsers()
        this.users = await Promise.all(
          ids.map(async ({ user_id }) => {
            const user = await authService.getUser(user_id)
            return {
              id: user.user_id,
              email: user.email,
              role: user.role,
              status: user.status,
            }
          }),
        )
      } finally {
        this.loading = false
      }
    },

    async setRole(id: string, role: ApiUserRole) {
      await authService.updateUser({ user_id: id, role })
      const user = this.users.find((u) => u.id === id)
      if (user) user.role = role
    },

    async setStatus(id: string, status: ApiUserStatus) {
      await authService.updateUser({ user_id: id, status })
      const user = this.users.find((u) => u.id === id)
      if (user) user.status = status
    },

    async updateEmail(id: string, email: string) {
      await authService.updateUser({ user_id: id, email })
      const user = this.users.find((u) => u.id === id)
      if (user) user.email = email
    },

    async updatePassword(id: string, newPassword: string) {
      await authService.updateUser({ user_id: id, new_password: newPassword })
    },
  },
})

export { useUsersStore }
