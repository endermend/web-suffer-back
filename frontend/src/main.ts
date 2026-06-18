import './assets/main.css'

import { createApp } from 'vue'
import router from './router/router.ts'
import App from './App.vue'
import { createPinia } from 'pinia'
// import './services/api/interceptors'

const pinia = createPinia()

createApp(App).use(pinia).use(router).mount('#app')
