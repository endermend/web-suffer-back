<template>
  <component :is="currentLayout">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

defineOptions({ name: 'App' })

const route = useRoute()

const currentLayout = computed(() =>
  route.meta.layout === 'auth' ? AuthLayout : DefaultLayout
)
</script>
