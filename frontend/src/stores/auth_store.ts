import { defineStore } from 'pinia'
import authService from '@/services/api/auth_service.ts'
import type { AuthCredentials, AuthToken, UserRole } from '@/types/auth.ts'

const useAuthStore = defineStore('auth', {
  state: () => ({
    // refresh token lives in an httpOnly cookie (sent automatically via withCredentials), never in JS-accessible storage
    accessToken: localStorage.getItem('access_token') || null,
    userEmail: localStorage.getItem('user_email') || null,
    // TODO: replace with role from API once roles exist on the backend
    role: (localStorage.getItem('role') as UserRole) || 'member',
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
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

        await this.fetchUserEmail()

        return { success: true, tokens }
      } catch (error: any) {
        this.error = error.message
        return { success: false, error: error.message }
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

    async fetchUserEmail() {
      try {
        const data = await authService.getEmail()
        this.userEmail = data.email
        localStorage.setItem('user_email', data.email)
      } catch (error) {
        console.error('Failed to fetch email:', error)
      }
    },

    async logout() {
      this.accessToken = null
      this.userEmail = null
      this.role = 'member'
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_email')
      localStorage.removeItem('role')
    },

    // test-only role switch, triggered by the role dropdown in the profile
    setRole(role: UserRole) {
      this.role = role
      localStorage.setItem('role', this.role)
    },
  },
})

export { useAuthStore }
