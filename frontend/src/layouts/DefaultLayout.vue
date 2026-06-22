<template>
  <AppHeader />
  <slot />
  <AppFooter />
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useAuthStore } from '@/stores/auth_store.ts'
import { useNotificationsStore } from '@/stores/notifications_store.ts'

defineOptions({ name: 'DefaultLayout' })

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()

// Failsafe role/email refresh for every authenticated role
onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchUserData().catch((error) => console.error('Failed to refresh user data:', error))
    notificationsStore.startPolling()
  }
})

watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) notificationsStore.startPolling()
    else notificationsStore.stopPolling()
  },
)
</script>
