import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/aura-light-indigo/theme.css'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import App from './App.vue'
import router from './router';



import ToastService from 'primevue/toastservice';

const app = createApp(App)
app.use(PrimeVue)
app.use(ToastService);
app.use(router)
app.mount('#app')