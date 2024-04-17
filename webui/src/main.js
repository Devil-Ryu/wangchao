import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import App from './App.vue'


import ToastService from 'primevue/toastservice';

const app = createApp(App)
app.use(PrimeVue)
app.use(ToastService);
app.mount('#app')