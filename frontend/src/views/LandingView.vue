<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { navAuth, navLogout } from '../services/navAuth.js'

const router = useRouter()
const tools = ref([])
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
      tools.value = data.tools
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

async function signOut() {
  await navLogout()
  loadTools()
}

onMounted(() => {
  loadTools()
  window.syncThemeButtons?.()
})
</script>

<template>
  <div class="landing">
    <header class="landing-header">
      <div class="brand">PLANETY</div>
      <div class="header-actions">
        <button class="ghost-btn" type="button" data-theme-toggle @click="toggleTheme">🌙</button>
        <template v-if="!navAuth.user">
          <button class="solid-btn" type="button" @click="toLogin">登录</button>
        </template>
        <template v-else>
          <span class="nav-user-info">{{ navAuth.user.username }}</span>
          <button class="ghost-btn" type="button" @click="signOut">退出</button>
        </template>
      </div>
    </header>

    <section class="hero">
      <div class="hero-title">PLANETY</div>
    </section>

    <main class="landing-main">
      <div v-if="error" class="alert alert-error" style="display:block">{{ error }}</div>

      <section class="tool-section">
        <div class="section-title">TOOLS</div>
        <div v-if="loading" class="empty-state"><p>Loading…</p></div>
        <div v-else-if="!tools.length" class="empty-state"><p>No tools available</p></div>
        <div v-else class="tool-grid">
          <article v-for="tool in tools" :key="tool.id" class="tool-card" @click="openTool(tool)">
            <div class="tool-icon">{{ tool.icon || '🔧' }}</div>
            <div class="tool-name">{{ tool.name }}</div>
          </article>
        </div>
      </section>
    </main>

    <footer class="landing-footer">
      <div class="footer-subtitle">I was the shadow of the waxwing slain<br />By the false azure in the windowpane</div>
    </footer>
  </div>
</template>

<style scoped>
/* 默认浅色主题 */
.landing {
  min-height: 100vh;
  color: #334155;
  background: linear-gradient(160deg, #eef3fb 0%, #f8fbff 50%, #eaf1fb 100%);
  display: flex;
  flex-direction: column;
  transition: background .3s, color .3s;
}
.landing::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  transition: opacity .3s;
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
  border-bottom: 1px solid rgba(15, 23, 42, .08);
}
.brand { font-size: 1.25rem; font-weight: 700; letter-spacing: 1px; color: #1e293b; }
.header-actions { display: flex; align-items: center; gap: 12px; }
.ghost-btn, .solid-btn {
  padding: 7px 16px; border-radius: 8px; border: 1px solid rgba(15,23,42,.25);
  background: transparent; color: #334155; cursor: pointer; font-size: .9rem;
  transition: all .2s;
}
.ghost-btn:hover { background: rgba(15, 23, 42, .08); }
.solid-btn { background: #3b82f6; border-color: #3b82f6; font-weight: 600; color: #fff; }
.solid-btn:hover { background: #2f6fe0; }
.nav-user-info { font-size: .9rem; color: #64748b; }
.hero {
  position: relative;
  text-align: center;
  padding: 26px 20px 18px;
}
.hero-title {
  font-size: 2.3rem; font-weight: 800; letter-spacing: 5px;
  background: linear-gradient(90deg, #1d4ed8, #3b82f6, #1d4ed8);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.landing-main {
  position: relative;
  flex: 1;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  padding: 8px 24px 48px;
  box-sizing: border-box;
}
.tool-section { margin-top: 26px; }
.section-title {
  font-size: 1.1rem; font-weight: 700; margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px; color: #1e293b; letter-spacing: 2px;
}
.tool-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 14px;
}
.tool-card {
  background: rgba(255,255,255,.75);
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 12px;
  padding: 16px 12px;
  text-align: center;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s, border-color .2s;
}
.tool-card:hover {
  transform: translateY(-4px);
  border-color: #3b82f6;
  box-shadow: 0 10px 26px rgba(59,130,246,.18);
}
.tool-icon { font-size: 1.5rem; margin-bottom: 8px; }
.tool-name { font-size: .95rem; font-weight: 700; color: #1e293b; }
.empty-state {
  background: rgba(15,23,42,.04);
  border: 1px dashed rgba(15,23,42,.15);
  border-radius: 12px;
  padding: 26px; text-align: center; color: #64748b;
}
.landing-footer {
  position: relative;
  text-align: center; padding: 22px 20px 18px; font-size: .8rem; color: #94a3b8;
  border-top: 1px solid rgba(15,23,42,.06);
}
.footer-subtitle {
  margin-bottom: 6px; font-size: .9rem; color: #64748b;
  letter-spacing: .5px; line-height: 1.5;
}

/* 深色主题覆盖 */
[data-theme="dark"] .landing {
  color: #e8ecf4;
  background: linear-gradient(160deg, #0b1026 0%, #14203f 45%, #1b2f55 100%);
}
[data-theme="dark"] .landing::before { opacity: 1; }
[data-theme="dark"] .landing-header {
  border-bottom: 1px solid rgba(255, 255, 255, .08);
  backdrop-filter: blur(6px);
}
[data-theme="dark"] .brand { color: #e8ecf4; }
[data-theme="dark"] .ghost-btn, [data-theme="dark"] .solid-btn {
  border-color: rgba(255,255,255,.25);
  color: #e8ecf4;
}
[data-theme="dark"] .ghost-btn:hover { background: rgba(255,255,255,.1); }
[data-theme="dark"] .nav-user-info { color: #c7d2fe; }
[data-theme="dark"] .hero-title {
  background: linear-gradient(90deg, #93c5fd, #e0f2fe, #93c5fd);
  -webkit-background-clip: text; background-clip: text;
}
[data-theme="dark"] .footer-subtitle { color: #a5b4d0; }
[data-theme="dark"] .section-title { color: #e0e7ff; }
[data-theme="dark"] .tool-card {
  background: rgba(255,255,255,.06);
  border-color: rgba(255,255,255,.12);
}
[data-theme="dark"] .tool-card:hover { border-color: rgba(147,197,253,.6); }
[data-theme="dark"] .tool-name { color: #f1f5f9; }
[data-theme="dark"] .empty-state {
  background: rgba(255,255,255,.04);
  border-color: rgba(255,255,255,.15);
  color: #8fa3c4;
}
[data-theme="dark"] .landing-footer {
  color: #64748b;
  border-top: 1px solid rgba(255,255,255,.06);
}
</style>
