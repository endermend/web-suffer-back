<template>
  <div class="card profile_hero">
    <div class="avatar">{{ avatarLetter }}</div>
    <div class="profile_info">
      <span class="profile_email">{{ emailLocalPart }}<wbr />{{ emailDomainPart }}</span>
      <span class="profile_role">{{ authStore.role }}</span>
    </div>

    <div
      v-if="authStore.role !== 'admin'"
      class="settings_trigger"
      @mouseenter="isSettingsMenuOpen = true"
      @mouseleave="isSettingsMenuOpen = false"
    >
      <RouterLink to="/settings" class="gear_link">
        <GearIcon class="gear_icon" :class="{ rotated: isSettingsMenuOpen }" />
      </RouterLink>

      <transition name="fade" mode="out-in">
        <span v-if="!isSettingsMenuOpen" class="settings_label">Настройки аккаунта</span>
        <div v-else class="settings_menu">
          <RouterLink to="/settings" class="settings_menu_item">
            <PenIcon class="settings_menu_icon" />
            <span>Сменить почту или пароль</span>
          </RouterLink>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth_store.ts'
import GearIcon from '@/assets/icons/gear.svg'
import PenIcon from '@/assets/icons/pen.svg'

defineOptions({ name: 'ProfileHero' })

// the failsafe refresh now lives in DefaultLayout so it covers every role
// (admin included, which has no profile page to do this from)
const authStore = useAuthStore()

const isSettingsMenuOpen = ref(false)

const userEmail = computed(function () {
  return authStore.userEmail ?? ''
})

const avatarLetter = computed(function () {
  return userEmail.value.charAt(0).toUpperCase() || '?'
})

const emailLocalPart = computed(function () {
  return userEmail.value.split('@')[0] ?? ''
})

const emailDomainPart = computed(function () {
  const atIndex = userEmail.value.indexOf('@')
  return atIndex === -1 ? '' : userEmail.value.slice(atIndex)
})
</script>

<style scoped>
.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.profile_hero {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 32px;
  padding: 24px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: rgb(160, 125, 180);
  color: white;
  font-family: Nagel;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  user-select: none;
}

.profile_info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-left: 8px;
  min-width: 0;
  flex: 1 1 auto;
}

.profile_email {
  font-family: Nagel;
  font-size: 20px;
  color: rgb(65, 65, 65);
  word-break: break-word;
}

.profile_role {
  appearance: none;
  border: none;
  outline: none;
  background: none;
  padding: 0;
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

/* settings trigger */

.settings_trigger {
  margin-left: auto;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  gap: 12px;
}

.settings_label {
  text-align: right;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  /* white-space: nowrap; */
  text-decoration: underline;
}

.gear_link {
  display: flex;
  cursor: pointer;
}

.gear_icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  color: rgb(160, 125, 180);
  transition:
    transform 0.25s ease,
    color 0.15s;
}

.gear_link:hover .gear_icon {
  color: rgb(140, 105, 160);
}

.gear_icon.rotated {
  transform: rotate(90deg);
}

.settings_menu {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* align-items: flex-end; */
  height: 64px;
}

.settings_menu_item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: Nagel;
  font-size: 13px;
  color: rgb(65, 65, 65);
  text-decoration: none;
  /* white-space: nowrap; */
  transition: color 0.15s;
}

.settings_menu_item:hover {
  color: rgb(160, 125, 180);
}

.settings_menu_icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: rgb(160, 125, 180);
}

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.2s,
    transform 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(8px);
}

@media screen and (max-width: 540px) {
  .profile_email {
    font-size: 4.5vw;
  }

  .avatar {
    height: 12vw;
    width: 12vw;
  }
}
</style>
