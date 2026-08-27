<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { setNavUser } from '../services/navAuth.js'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const error = ref('')
const submitting = ref(false)

async function submit() {
  error.value = ''
  submitting.value = true
  const body = new FormData()
  body.append('username', form.username)
  body.append('password', form.password)
  try {
    const res = await fetch('/api/nav/login', { method: 'POST', body, credentials: 'include' })
    const data = await res.json()
    submitting.value = false
    if (!data.success) return (error.value = data.message)
    setNavUser(data.user)
    router.push('/')
  } catch (e) {
    submitting.value = false
    error.value = '网络错误，请稍后重试'
  }
}
</script>

<template>
  <main class="auth-page">
    <div class="auth-card">
      <h1>🛫 停机坪</h1>
      <p class="subtitle">登录以查看私人工具</p>
      <div v-if="error" class="alert alert-error" style="display:block">{{ error }}</div>
      <form @submit.prevent="submit">
        <div class="form-group"><label>用户名</label><input v-model.trim="form.username" required autofocus placeholder="请输入用户名" /></div>
        <div class="form-group"><label>密码</label><input v-model="form.password" type="password" required placeholder="请输入密码" /></div>
        <button class="btn btn-primary" :disabled="submitting">{{ submitting ? '登录中…' : '登 录' }}</button>
      </form>
      <p class="auth-footer">还没有账号？<RouterLink to="/nav/register">注册一个</RouterLink> · <RouterLink to="/">返回首页</RouterLink></p>
    </div>
  </main>
</template>
