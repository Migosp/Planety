import { reactive } from 'vue'

// PLANETY 导航站独立登录态（与评分工具 art-user 互不干扰）
function stored() {
  try { return JSON.parse(localStorage.getItem('nav-user')) } catch { return null }
}

export const navAuth = reactive({ user: stored() })

export function setNavUser(user) {
  navAuth.user = user
  if (user) localStorage.setItem('nav-user', JSON.stringify(user))
  else localStorage.removeItem('nav-user')
}

export async function navLogout() {
  await fetch('/api/nav/logout', { method: 'POST', credentials: 'include' })
  setNavUser(null)
}
