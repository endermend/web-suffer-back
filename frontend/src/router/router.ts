import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store.ts'
import type { UserRole } from '@/types/auth.ts'
import DashboardPage from '@/pages/DashboardPage.vue'
import TasksPage from '@/pages/contender/TasksPage.vue'
import AllTasksPage from '@/pages/contender/AllTasksPage.vue'
import TaskDetailPage from '@/pages/contender/TaskDetailPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import ProfilePage from '@/pages/contender/ProfilePage.vue'
import SettingsPage from '@/pages/SettingsPage.vue'
import ManageTasksPage from '@/pages/admin/ManageTasksPage.vue'
import TaskReviewPage from '@/pages/admin/TaskReviewPage.vue'
import UsersPage from '@/pages/admin/UsersPage.vue'
import AdminProfilePage from '@/pages/admin/AdminProfilePage.vue'
import NotFoundPage from '@/pages/NotFoundPage.vue'
import ForbiddenPage from '@/pages/ForbiddenPage.vue'

// `roles` restricts a route to the listed roles. Admin bypasses this check (can
// factually visit any page) unless `adminBypass: false` is set explicitly — used
// for routes like /settings that are functionally meaningless for admins, since
// they can't change their own email/password.
declare module 'vue-router' {
  interface RouteMeta {
    layout: 'default' | 'auth'
    roles?: UserRole[]
    adminBypass?: boolean
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardPage, meta: { layout: 'default' } },
    { path: '/tasks', component: TasksPage, meta: { layout: 'default' } },
    { path: '/tasks/all', component: AllTasksPage, meta: { layout: 'default' } },
    { path: '/tasks/:id', component: TaskDetailPage, meta: { layout: 'default' } },
    { path: '/profile', component: ProfilePage, meta: { layout: 'default' } },
    {
      path: '/settings',
      component: SettingsPage,
      meta: { layout: 'default', roles: ['member', 'moderator'], adminBypass: false },
    },
    {
      path: '/admin/tasks',
      component: ManageTasksPage,
      meta: { layout: 'default', roles: ['admin', 'moderator'] },
    },
    {
      path: '/admin/submissions/:id/review',
      component: TaskReviewPage,
      meta: { layout: 'default', roles: ['admin', 'moderator'] },
    },
    {
      path: '/admin/users',
      component: UsersPage,
      meta: { layout: 'default', roles: ['admin'] },
    },
    {
      path: '/admin/profile',
      component: AdminProfilePage,
      meta: { layout: 'default', roles: ['admin', 'moderator'] },
    },
    { path: '/login', component: LoginPage, meta: { layout: 'auth' } },
    { path: '/register', component: RegisterPage, meta: { layout: 'auth' } },
    { path: '/403', component: ForbiddenPage, meta: { layout: 'auth' } },
    { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { layout: 'auth' } },
  ],
})

router.beforeEach((to) => {
  if (!to.meta.roles) return true

  const authStore = useAuthStore()
  if (to.meta.adminBypass !== false && authStore.role === 'admin') return true

  return to.meta.roles.includes(authStore.role) ? true : '/403'
})

export default router
