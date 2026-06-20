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
import ManageTasksPage from '@/pages/moderator/ManageTasksPage.vue'
import CreateTaskPage from '@/pages/moderator/CreateTaskPage.vue'
import TaskReviewPage from '@/pages/moderator/TaskReviewPage.vue'
import ModeratorProfilePage from '@/pages/moderator/ModeratorProfilePage.vue'
import UsersPage from '@/pages/admin/UsersPage.vue'
import NotFoundPage from '@/pages/NotFoundPage.vue'
import ForbiddenPage from '@/pages/ForbiddenPage.vue'

// `roles` restricts a route to the listed roles. Admin bypasses this check (can
// factually visit any page) unless `adminBypass: false` is set explicitly — used
// for routes like /settings that are functionally meaningless for admins, since
// they can't change their own email/password.
// `public` marks a route as reachable without being logged in — everything else
// is 403 for unauthenticated visitors. 404 and 403 themselves are always reachable.
declare module 'vue-router' {
  interface RouteMeta {
    layout: 'default' | 'auth'
    roles?: UserRole[]
    adminBypass?: boolean
    public?: boolean
  }
}

const NOT_FOUND_PATH = '/:pathMatch(.*)*'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition ?? { top: 0 }
  },
  routes: [
    { path: '/', component: DashboardPage, meta: { layout: 'default', public: true } },
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
      path: '/moderator/tasks',
      component: ManageTasksPage,
      meta: { layout: 'default', roles: ['moderator'], adminBypass: false },
    },
    {
      path: '/moderator/tasks/create',
      component: CreateTaskPage,
      meta: { layout: 'default', roles: ['moderator'], adminBypass: false },
    },
    {
      path: '/moderator/tasks/:id/edit',
      component: CreateTaskPage,
      meta: { layout: 'default', roles: ['moderator'], adminBypass: false },
    },
    {
      path: '/moderator/submissions/:id/review',
      component: TaskReviewPage,
      meta: { layout: 'default', roles: ['moderator'], adminBypass: false },
    },
    {
      path: '/moderator/profile',
      component: ModeratorProfilePage,
      meta: { layout: 'default', roles: ['moderator'], adminBypass: false },
    },
    {
      path: '/admin/users',
      component: UsersPage,
      meta: { layout: 'default', roles: ['admin'] },
    },
    { path: '/login', component: LoginPage, meta: { layout: 'auth', public: true } },
    { path: '/register', component: RegisterPage, meta: { layout: 'auth', public: true } },
    { path: '/403', component: ForbiddenPage, meta: { layout: 'auth' } },
    { path: NOT_FOUND_PATH, component: NotFoundPage, meta: { layout: 'auth' } },
  ],
})

router.beforeEach((to) => {
  // error pages are always reachable, regardless of auth state — otherwise a
  // redirect to /403 for a guest could itself loop back into another redirect
  if (to.path === '/403' || to.matched.some((r) => r.path === NOT_FOUND_PATH)) return true

  const authStore = useAuthStore()

  if (!authStore.isAuthenticated) {
    return to.meta.public ? true : '/403'
  }

  if (!to.meta.roles) return true
  if (to.meta.adminBypass !== false && authStore.role === 'admin') return true

  return to.meta.roles.includes(authStore.role) ? true : '/403'
})

export default router
