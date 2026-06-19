<template>
  <header>
    <!-- upper header -->
    <div class="header_upper">
      <div class="header_upper_contents">
        <RouterLink to="/" class="logo_main">
          <img src="@/assets/images/mainlogo.png" />
          <span>web-suffer-front</span>
        </RouterLink>

        <div class="account_main">
          <template v-if="!isAuthenticated">
            <div @click="router.push('/login')">
              <PersonIcon />
            </div>
          </template>

          <template v-else>
            <div ref="bellIconRef" @click="toggleNotifications">
              <BellIcon />
            </div>

            <div ref="logoutBtnRef" @click="toggleLogoutConfirm">
              <span class="logout_text">Выход</span>
            </div>

            <span @click="router.push(profileLink)" class="user_email">{{ userEmail }}</span>
          </template>
        </div>
      </div>
    </div>

    <!-- confirm exit -->
    <div
      v-if="isLogoutConfirm"
      ref="logoutConfirmPanelRef"
      class="logout_confirm_panel"
      :style="logoutConfirmStyle"
    >
      <span class="logout_confirm_text">Выйти из аккаунта?</span>
      <button @click="confirmLogout" type="button">Да</button>
      <button @click="isLogoutConfirm = false" type="button">Нет</button>
    </div>

    <!-- notif -->
    <div
      v-if="isNotificationsOpen"
      ref="notificationsPanelRef"
      class="notifications_panel"
      :style="notificationsPanelStyle"
    >
      <div v-if="notifications.length === 0" class="notifications_empty">Нет уведомлений</div>
      <div v-for="notification in notifications" :key="notification.id" class="notification_item">
        {{ notification.message }}
      </div>
    </div>

    <!-- lower header -->
    <div v-if="isDesktop || isTablet" class="header_lower">
      <nav class="nav_desktop">
        <RouterLink
          to="/"
          @click="toggleNavJump('/')"
          :class="{ jump: jumpingPath === '/' }"
          @animationend="jumpingPath = null"
          >Новости</RouterLink
        >
        <RouterLink
          to="/tasks"
          v-if="authStore.role === 'member' && isAuthenticated"
          @click="toggleNavJump('/tasks')"
          :class="{ jump: jumpingPath === '/tasks' }"
          @animationend="jumpingPath = null"
          >Задания</RouterLink
        >
        <RouterLink
          to="/admin/tasks"
          v-if="authStore.role === 'moderator' && isAuthenticated"
          @click="toggleNavJump('/admin/tasks')"
          :class="{ jump: jumpingPath === '/admin/tasks' }"
          @animationend="jumpingPath = null"
          >Управление заданиями</RouterLink
        >
        <RouterLink
          to="/admin/users"
          v-if="authStore.role === 'admin' && isAuthenticated"
          @click="toggleNavJump('/admin/users')"
          :class="{ jump: jumpingPath === '/admin/users' }"
          @animationend="jumpingPath = null"
          >Пользователи</RouterLink
        >
        <RouterLink
          :to="profileLink"
          v-if="isAuthenticated"
          @click="toggleNavJump(profileLink)"
          :class="{ jump: jumpingPath === profileLink }"
          @animationend="jumpingPath = null"
          >Профиль</RouterLink
        >
      </nav>
    </div>

    <!-- mobile nav -->
    <div v-if="isMobile" class="mobile_footer">
      <nav class="nav_mobile">
        <RouterLink
          to="/"
          @click="toggleNavJump('/')"
          :class="{ jump: jumpingPath === '/' }"
          @animationend="jumpingPath = null"
          >Новости</RouterLink
        >
        <RouterLink
          to="/tasks"
          v-if="authStore.role === 'member' && isAuthenticated"
          @click="toggleNavJump('/tasks')"
          :class="{ jump: jumpingPath === '/tasks' }"
          @animationend="jumpingPath = null"
          >Задания</RouterLink
        >
        <RouterLink
          to="/admin/tasks"
          v-if="authStore.role === 'moderator' && isAuthenticated"
          @click="toggleNavJump('/admin/tasks')"
          :class="{ jump: jumpingPath === '/admin/tasks' }"
          @animationend="jumpingPath = null"
          >Управление заданиями</RouterLink
        >
        <RouterLink
          :to="profileLink"
          v-if="isAuthenticated"
          @click="toggleNavJump(profileLink)"
          :class="{ jump: jumpingPath === profileLink }"
          @animationend="jumpingPath = null"
          >Профиль</RouterLink
        >
        <RouterLink
          to="/admin/users"
          v-if="authStore.role === 'admin' && isAuthenticated"
          @click="toggleNavJump('/admin/users')"
          :class="{ jump: jumpingPath === '/admin/users' }"
          @animationend="jumpingPath = null"
          >Пользователи</RouterLink
        >
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store.ts'
import { useBreakpoints, onClickOutside } from '@vueuse/core'
import PersonIcon from '@/assets/icons/person.svg'
import BellIcon from '@/assets/icons/bell.svg'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userEmail = computed(() => authStore.userEmail)
const profileLink = computed(() =>
  authStore.role === 'admin' || authStore.role === 'moderator' ? '/admin/profile' : '/profile',
)

// anims

const jumpingPath = ref<string | null>(null)

async function toggleNavJump(path: string) {
  await nextTick()
  jumpingPath.value = path
}

// javascript adaptivity

const breakpoints = useBreakpoints({
  mobile: 0,
  tablet: 540,
  desktop: 1050,
})

const isDesktop = breakpoints.greater('desktop')
const isTablet = breakpoints.between('tablet', 'desktop')
const isMobile = breakpoints.smaller('tablet')

const notificationsPanelRef = ref<HTMLDivElement | null>(null)
const logoutConfirmPanelRef = ref<HTMLDivElement | null>(null)

// panel position

const VIEWPORT_MARGIN = 8

function clampPanelLeft(left: number, panelWidth: number): number {
  const maxLeft = window.innerWidth - panelWidth - VIEWPORT_MARGIN
  return Math.min(Math.max(left, VIEWPORT_MARGIN), maxLeft)
}

// notifications

const bellIconRef = ref<HTMLDivElement | null>(null)
const isNotificationsOpen = ref(false)
const bellCoords = ref({ top: 0, left: 0 })
const notifications = ref<Array<{ id: number; message: string }>>([])
const NOTIFICATIONS_PANEL_WIDTH = 250

function toggleNotifications(): void {
  const rect = bellIconRef.value!.getBoundingClientRect()
  bellCoords.value = {
    top: rect.bottom + 5,
    left: clampPanelLeft(rect.left - 4, NOTIFICATIONS_PANEL_WIDTH),
  }
  isNotificationsOpen.value = !isNotificationsOpen.value
  isLogoutConfirm.value = false
}

const notificationsPanelStyle = computed(() => ({
  position: 'fixed' as const,
  top: `${bellCoords.value.top}px`,
  left: `${bellCoords.value.left}px`,
}))

// --- logout ---

const logoutBtnRef = ref<HTMLDivElement | null>(null)
const isLogoutConfirm = ref(false)
const logoutCoords = ref({ top: 0, left: 0 })
const LOGOUT_CONFIRM_PANEL_WIDTH = 180

function toggleLogoutConfirm(): void {
  const rect = logoutBtnRef.value!.getBoundingClientRect()
  logoutCoords.value = {
    top: rect.bottom + 5,
    left: clampPanelLeft(rect.left - 4, LOGOUT_CONFIRM_PANEL_WIDTH),
  }
  isLogoutConfirm.value = !isLogoutConfirm.value
  isNotificationsOpen.value = false
}

const logoutConfirmStyle = computed(() => ({
  position: 'fixed' as const,
  top: `${logoutCoords.value.top}px`,
  left: `${logoutCoords.value.left}px`,
}))

function confirmLogout(): void {
  router.push('/')
  authStore.logout()
  isLogoutConfirm.value = false
}

// --- click outside ---

onClickOutside(notificationsPanelRef, () => (isNotificationsOpen.value = false), {
  ignore: [bellIconRef],
})
onClickOutside(logoutConfirmPanelRef, () => (isLogoutConfirm.value = false), {
  ignore: [logoutBtnRef],
})
</script>

<style scoped>
header {
  z-index: 2;
  position: fixed;
  width: 100%;
}

/* Transition */

/* logout confirmation */

.logout_confirm_panel {
  border-radius: 8px;
  position: fixed;
  width: 180px;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  background-color: white;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
}

.logout_confirm_text {
  padding: 16px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  border-bottom: thin solid rgb(230, 228, 240);
}

.logout_confirm_panel button {
  width: 100%;
  font-family: Nagel;
  padding: 16px 20px;
  background-color: white;
  transition: 0.2s background-color;
  cursor: pointer;
  appearance: none;
  background: none;
  border: none;
  outline: none;
  text-align: left;
}

.logout_confirm_panel button:hover {
  background-color: rgb(160, 125, 180);
  color: white;
}

/* notifications panel */

.notifications_panel {
  position: fixed;
  width: 250px;
  z-index: 5;
  display: flex;
  flex-direction: column;
  background-color: white;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.notifications_empty {
  user-select: none;
  padding: 20px 16px;
  font-family: Nagel;
  color: rgb(150, 150, 150);
  text-align: center;
}

.notification_item {
  user-select: none;
  padding: 12px 16px;
  font-family: Nagel;
  border-bottom: thin solid rgb(230, 230, 230);
}

/* upper header */

.header_upper {
  position: relative;
  height: 70px;
  display: flex;
  justify-content: center;
  z-index: 6;
  background-color: rgb(160, 125, 180);
}

.header_upper_contents {
  width: 1000px;
  display: flex;
  justify-content: space-between;
}

/* logo */

.logo_main {
  display: flex;
  align-items: center;
  padding-inline: 10px;
  cursor: pointer;
  text-decoration: none;
}

.logo_main img {
  height: 90%;
}

.logo_main span {
  color: white;
  font-size: 24px;
  margin-left: 8px;
  font-family: Nagel;
}

/* account */

.account_main {
  font-size: 24px;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
}

.account_main div {
  padding-block: 10px;
  padding-inline: 4px;
  height: 100%;
  display: flex;
  align-items: center;
}

.account_main div svg {
  color: white;
  width: 100%;
  height: 100%;
  cursor: pointer;
  min-width: 32px;
  transition: 0.2s transform;
}

.account_main div svg:hover {
  transform: scale(1.1);
}

.logout_text {
  user-select: none;
  color: black;
  font-family: Nagel;
  font-size: 16px;
  padding-block: 8px;
  padding-inline: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  border-radius: 24px;
  background-color: white;
  cursor: pointer;
  display: inline-block;
  transition: 0.2s transform;
}

.logout_text:hover {
  transform: scale(1.06);
}

.user_email {
  user-select: none;
  color: white;
  font-size: 20px;
  font-family: Nagel;
  cursor: pointer;
  margin-inline: 8px;
  white-space: nowrap;
  display: inline-block;
  transition: 0.2s transform;
}

.user_email:hover {
  transform: scale(1.06);
}

/* lower header */

.header_lower {
  position: relative;
  height: 100px;
  z-index: 4;
  display: flex;
  justify-content: center;
  background-color: rgb(255, 255, 255);
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
}

.nav_desktop {
  display: flex;
  width: 1000px;
  align-items: center;
}

.nav_desktop a {
  user-select: none;
  height: 32px;
  font-size: 20px;
  margin-inline: 10px;
  align-content: center;
  font-family: Nagel;
  cursor: pointer;
  color: rgb(65, 65, 65);
  border-bottom: solid thin rgb(65, 65, 65);
  text-decoration: none;
}

.nav_desktop a.jump {
  animation: jump 0.4s ease;
}
@keyframes jump {
  0% {
    transform: translateY(0px);
  }
  30% {
    transform: translateY(-16px);
  }
  0% {
    transform: translateY(0px);
  }
}

.nav_desktop a.router-link-active {
  color: rgb(160, 125, 180);
  border-bottom-color: rgb(160, 125, 180);
}

/* mobile navigation */

.mobile_footer {
  width: 100%;
  position: fixed;
  bottom: 0;
  height: 100px;
  z-index: 4;
  display: flex;
  justify-content: center;
  background-color: rgb(255, 255, 255);
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
}

.nav_mobile {
  display: flex;
  justify-content: space-evenly;
  width: 1000px;
  align-items: center;
}

.nav_mobile a {
  height: 32px;
  font-size: 20px;
  margin-inline: 10px;
  align-content: center;
  font-family: Nagel;
  cursor: pointer;
  color: rgb(65, 65, 65);
  border-bottom: solid thin rgb(65, 65, 65);
  text-decoration: none;
}

.nav_mobile a.router-link-active {
  color: rgb(160, 125, 180);
  border-bottom-color: rgb(160, 125, 180);
}

@media screen and (max-width: 1050px) and (min-width: 540px) {
  .header_upper_contents {
    width: 100%;
  }
}

@media screen and (max-width: 540px) {
  .header_upper {
    box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
  }

  .logo_main span {
    font-size: 4vw;
  }

  .user_email {
    font-size: 4vw;
  }
}
</style>
