import { createRouter, createWebHistory } from "vue-router";
import DetectProtectMaskPage from '../views/DetectProtectMaskPage.vue';
import Home from '../views/Home.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/protect', component: DetectProtectMaskPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes: [...routes]
});


export default router;