import { createRouter, createWebHistory } from 'vue-router'
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

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardPage, meta: { layout: 'default' } },
    { path: '/tasks', component: TasksPage, meta: { layout: 'default' } },
    { path: '/tasks/all', component: AllTasksPage, meta: { layout: 'default' } },
    { path: '/tasks/:id', component: TaskDetailPage, meta: { layout: 'default' } },
    { path: '/profile', component: ProfilePage, meta: { layout: 'default' } },
    { path: '/settings', component: SettingsPage, meta: { layout: 'default' } },
    { path: '/admin/tasks', component: ManageTasksPage, meta: { layout: 'default' } },
    { path: '/admin/tasks/:id/review', component: TaskReviewPage, meta: { layout: 'default' } },
    { path: '/admin/users', component: UsersPage, meta: { layout: 'default' } },
    { path: '/admin/profile', component: AdminProfilePage, meta: { layout: 'default' } },
    { path: '/login', component: LoginPage, meta: { layout: 'auth' } },
    { path: '/register', component: RegisterPage, meta: { layout: 'auth' } },
  ],
})

export default router
