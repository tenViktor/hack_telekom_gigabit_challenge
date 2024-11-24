// main.ts
import '../assets/main.css'  // Change the path to be relative to the src directory
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { defineCustomElements } from '@telekom/scale-components/loader'
import '@telekom/scale-components/dist/scale-components/scale-components.css'
import App from '../App.vue'
import router from '../router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

defineCustomElements()
app.mount('#app')