import { defineStore } from 'pinia'
import authService from '@/services/api/auth_service.ts'
import type { ApiUserStatus, AuthCredentials, AuthToken, UserRole } from '@/types/auth.ts'

const useAuthStore = defineStore('auth', {
  state: () => ({
    // refresh token lives in an httpOnly cookie (sent automatically via withCredentials), never in JS-accessible storage
    accessToken: localStorage.getItem('access_token') || null,
    userEmail: localStorage.getItem('user_email') || null,
    // TODO: replace with role from API once roles exist on the backend
    role: (localStorage.getItem('role') as UserRole) || 'member',
    userStatus: (localStorage.getItem('user_status') as ApiUserStatus) || 'active',
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,

    // Where each role should land right after login/register.
    landingPath: (state): string => {
      if (state.role === 'moderator') return '/moderator/tasks'
      if (state.role === 'admin') return '/admin/users'
      return '/tasks'
    },
  },

  actions: {
    // register
    async register({ email, password }: AuthCredentials) {
      this.loading = true
      this.error = null
      // a fresh session always starts as a plain member, even if a role was
      // left over in localStorage from a previous session's dev role-switcher
      this.role = 'member'
      localStorage.setItem('role', this.role)

      try {
        const tokens = await authService.register({ email, password })
        this.setAccessToken(tokens)
        return { success: true, tokens }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.loading = false
      }
    },

    // login
    async login({ email, password }: AuthCredentials) {
      this.loading = true
      this.error = null
      // a fresh session always starts as a plain member, even if a role was
      // left over in localStorage from a previous session's dev role-switcher
      this.role = 'member'
      localStorage.setItem('role', this.role)

      try {
        const tokens = await authService.login({ email, password })
        this.setAccessToken(tokens)

        await this.fetchUserData()

        if (this.userStatus === 'banned') {
          await this.logout()
          return { success: false, banned: true, error: 'Этот аккаунт временно заблокирован' }
        }

        return { success: true, tokens }
      } catch (error: any) {
        this.error = error.message
        return { success: false, banned: false, error: error.message }
      } finally {
        this.loading = false
      }
    },

    // save access token to localStorage — auth_service's apiClient reads it from there
    // on every request, so there's no separate header to keep in sync here
    setAccessToken(tokens: AuthToken) {
      this.accessToken = tokens.access_token
      localStorage.setItem('access_token', tokens.access_token)
    },

    // Doesn't catch its own errors — a confirmed invalid/expired token already
    // triggers logout() from the axios response interceptor once its own refresh
    // attempt fails. Swallowing errors here too would mean any transient network
    // or 5xx blip (e.g. right after login, before the token is even used elsewhere)
    // silently wipes out a perfectly valid session. Callers (login/register) already
    // handle a thrown error by surfacing it instead of pretending the call succeeded.
    async fetchUserData() {
      const data = await authService.getUser() // this user

      this.userEmail = data.email
      localStorage.setItem('user_email', data.email)

      this.userStatus = data.status
      localStorage.setItem('user_status', data.status)

      let role: UserRole
      if (data.role === 'admin' || data.role === 'moderator') {
        role = data.role
      } else {
        role = 'member'
      }
      this.role = role
      localStorage.setItem('role', role)
    },

    // self-service delete/restore — backend's CHANGE_SELF right now covers both
    // active and deleted status, so a deleted member can call this again to restore
    async setOwnStatus(status: 'active' | 'deleted') {
      await authService.updateUser({ status })
      this.userStatus = status
      localStorage.setItem('user_status', status)
    },

    async logout() {
      this.accessToken = null
      this.userEmail = null
      this.role = 'member'
      this.userStatus = 'active'
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_email')
      localStorage.removeItem('role')
      localStorage.removeItem('user_status')
    },
  },
})

export { useAuthStore }
