import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../services/auth.js'
import { navAuth } from '../services/navAuth.js'

const routes = [
  // 停机坪导航站（游客可访问）
  { path: '/', component: () => import('../views/LandingView.vue') },
  { path: '/nav/login', component: () => import('../views/NavLoginView.vue'), meta: { navGuest: true } },
  { path: '/nav/register', component: () => import('../views/NavRegisterView.vue'), meta: { navGuest: true } },
  // 艺术评分工具（挂载在 /art 前缀下）
  { path: '/art', component: () => import('../views/HomeView.vue'), meta: { auth: true } },
  { path: '/art/admin', component: () => import('../views/AdminView.vue'), meta: { auth: true, admin: true } },
  { path: '/art/upload', component: () => import('../views/UploadView.vue'), meta: { auth: true, admin: true } },
  { path: '/art/change-password', component: () => import('../views/ChangePasswordView.vue'), meta: { auth: true } },
  // 艺术评分工具登录/注册（保留原路径）
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to) => {
  // 评分工具登录态（art-user）
  if (to.meta.auth && !auth.user) return '/login'
  if (to.meta.admin && auth.user?.role !== 'admin') return '/art'
  if (to.meta.guest && auth.user) return auth.user.role === 'admin' ? '/art/admin' : '/art'
  // 导航站登录态（nav-user）
  if (to.meta.navGuest && navAuth.user) return '/'
})

export default router
