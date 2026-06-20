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

    // GET /api/auth/users only ever lists role='user' accounts — promoting someone
    // out of that role makes them drop out of this page, so drop them locally too
    // instead of leaving a stale row that only vanishes on the next reload.
    async setRole(id: string, role: ApiUserRole) {
      await authService.updateUser({ user_id: id, role })
      if (role === 'user') {
        const user = this.users.find((u) => u.id === id)
        if (user) user.role = role
      } else {
        this.users = this.users.filter((u) => u.id !== id)
      }
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

    async deleteUser(id: string) {
      await authService.updateUser({ user_id: id, status: 'deleted' })
      this.users = this.users.filter((u) => u.id !== id)
    },
  },
})

export { useUsersStore }
