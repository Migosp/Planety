<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { navAuth, navLogout } from '../services/navAuth.js'

const router = useRouter()
const publicTools = ref([])
const privateTools = ref([])
const loading = ref(true)
const error = ref('')
const toggleTheme = () => window.toggleTheme()

async function loadTools() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/tools', { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      publicTools.value = data.tools.filter(t => t.visibility === 'public')
      privateTools.value = data.tools.filter(t => t.visibility === 'private')
    } else {
      error.value = data.message || '加载失败'
    }
  } catch (e) {
    error.value = '网络异常，请稍后重试'
  }
  loading.value = false
}

function openTool(tool) {
  if (/^https?:\/\//.test(tool.url)) window.open(tool.url, '_blank')
  else router.push(tool.url)
}

function toLogin() { router.push('/nav/login') }
function toRegister() { router.push('/nav/register') }

async function signOut() {
  await navLogout()
  loadTools()
}

onMounted(loadTools)
</script>

<template>
  <div class="landing">
    <header class="landing-header">
      <div class="brand">🛫 停机坪</div>
      <div class="header-actions">
        <button class="ghost-btn" type="button" @click="toggleTheme">🌙</button>
        <template v-if="!navAuth.user">
          <button class="ghost-btn" type="button" @click="toLogin">登录</button>
          <button class="solid-btn" type="button" @click="toRegister">注册</button>
        </template>
        <template v-else>
          <span class="nav-user-info">{{ navAuth.user.username }}<template v-if="navAuth.user.role === 'admin'"> · 管理员</template></span>
          <button class="ghost-btn" type="button" @click="signOut">退出</button>
        </template>
      </div>
    </header>

    <section class="hero">
      <div class="hero-title">停机坪</div>
      <div class="hero-subtitle">起飞之前，先到这里看看 —— 各类工具的起飞入口</div>
    </section>

    <main class="landing-main">
      <div v-if="error" class="alert alert-error" style="display:block">{{ error }}</div>

      <section class="tool-section">
        <div class="section-title">✈️ 公共工具</div>
        <div v-if="loading" class="empty-state"><p>加载中…</p></div>
        <div v-else-if="!publicTools.length" class="empty-state"><p>暂无公共工具</p></div>
        <div v-else class="tool-grid">
          <article v-for="tool in publicTools" :key="tool.id" class="tool-card" @click="openTool(tool)">
            <div class="tool-icon">{{ tool.icon || '🔧' }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-enter">进入 →</div>
          </article>
        </div>
      </section>

      <section v-if="navAuth.user" class="tool-section">
        <div class="section-title">🔒 私人工具</div>
        <div v-if="!privateTools.length" class="empty-state"><div class="icon">🔐</div><p>暂无私人工具</p></div>
        <div v-else class="tool-grid">
          <article v-for="tool in privateTools" :key="tool.id" class="tool-card" @click="openTool(tool)">
            <div class="tool-icon">{{ tool.icon || '🔧' }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-enter">进入 →</div>
          </article>
        </div>
      </section>

      <section v-if="!navAuth.user" class="login-hint">
        <p>🔒 登录后可解锁私人工具</p>
        <button class="solid-btn" type="button" @click="toLogin">立即登录</button>
      </section>
    </main>

    <footer class="landing-footer">Planety · 停机坪 · 综合工具导航</footer>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  color: #e8ecf4;
  background: linear-gradient(160deg, #0b1026 0%, #14203f 45%, #1b2f55 100%);
  display: flex;
  flex-direction: column;
}
.landing::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image:
    radial-gradient(1.5px 1.5px at 12% 18%, rgba(255,255,255,.7), transparent 60%),
    radial-gradient(1px 1px at 34% 8%, rgba(255,255,255,.5), transparent 60%),
    radial-gradient(1.5px 1.5px at 58% 26%, rgba(255,255,255,.6), transparent 60%),
    radial-gradient(1px 1px at 76% 12%, rgba(255,255,255,.5), transparent 60%),
    radial-gradient(1.5px 1.5px at 88% 34%, rgba(255,255,255,.6), transparent 60%),
    radial-gradient(1px 1px at 22% 42%, rgba(255,255,255,.4), transparent 60%),
    radial-gradient(1.5px 1.5px at 68% 52%, rgba(255,255,255,.45), transparent 60%),
    radial-gradient(1px 1px at 92% 62%, rgba(255,255,255,.4), transparent 60%);
}
.landing-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 32px;
  border-bottom: 1px solid rgba(255, 255, 255, .08);
  backdrop-filter: blur(6px);
}
.brand { font-size: 1.25rem; font-weight: 700; letter-spacing: 1px; }
.header-actions { display: flex; align-items: center; gap: 12px; }
.ghost-btn, .solid-btn {
  padding: 7px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,.25);
  background: transparent; color: #e8ecf4; cursor: pointer; font-size: .9rem;
  transition: all .2s;
}
.ghost-btn:hover { background: rgba(255,255,255,.1); }
.solid-btn { background: #3b82f6; border-color: #3b82f6; font-weight: 600; }
.solid-btn:hover { background: #2f6fe0; }
.nav-user-info { font-size: .9rem; color: #c7d2fe; }
.hero {
  position: relative;
  text-align: center;
  padding: 64px 20px 40px;
}
.hero-title {
  font-size: 3.4rem; font-weight: 800; letter-spacing: 6px;
  background: linear-gradient(90deg, #93c5fd, #e0f2fe, #93c5fd);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero-subtitle { margin-top: 14px; color: #a5b4d0; font-size: 1.05rem; letter-spacing: 1px; }
.landing-main {
  position: relative;
  flex: 1;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  padding: 8px 24px 48px;
  box-sizing: border-box;
}
.tool-section { margin-top: 36px; }
.section-title {
  font-size: 1.1rem; font-weight: 700; margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px; color: #e0e7ff;
}
.tool-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 18px;
}
.tool-card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 14px;
  padding: 22px 18px;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s, border-color .2s;
}
.tool-card:hover {
  transform: translateY(-4px);
  border-color: rgba(147,197,253,.6);
  box-shadow: 0 10px 26px rgba(59,130,246,.18);
}
.tool-icon { font-size: 2rem; margin-bottom: 10px; }
.tool-name { font-size: 1.05rem; font-weight: 700; color: #f1f5f9; }
.tool-desc {
  margin-top: 6px; font-size: .85rem; color: #9fb0cd;
  min-height: 40px; line-height: 1.5;
}
.tool-enter { margin-top: 12px; font-size: .85rem; color: #93c5fd; font-weight: 600; }
.empty-state {
  background: rgba(255,255,255,.04);
  border: 1px dashed rgba(255,255,255,.15);
  border-radius: 12px;
  padding: 26px; text-align: center; color: #8fa3c4;
}
.empty-state .icon { font-size: 1.6rem; margin-bottom: 6px; }
.login-hint {
  margin-top: 40px; text-align: center; color: #a5b4d0;
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.landing-footer {
  position: relative;
  text-align: center; padding: 20px; font-size: .8rem; color: #64748b;
  border-top: 1px solid rgba(255,255,255,.06);
}
</style>
