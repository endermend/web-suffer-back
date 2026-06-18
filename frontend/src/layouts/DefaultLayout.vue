<template>
  <AppHeader />
  <slot />
  <AppFooter />
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

defineOptions({ name: 'DefaultLayout' })
</script>
