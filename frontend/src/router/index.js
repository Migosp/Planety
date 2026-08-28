import { createRouter, createWebHistory } from 'vue-router'
import { navAuth } from '../services/navAuth.js'

const routes = [
  // PLANETY 导航首页（游客可访问）
  { path: '/', component: () => import('../views/LandingView.vue') },
  // 导航站登录
  { path: '/nav/login', component: () => import('../views/NavLoginView.vue'), meta: { navGuest: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to) => {
  // 已登录导航站时不再进入登录页
  if (to.meta.navGuest && navAuth.user) return '/'
})

export default router
