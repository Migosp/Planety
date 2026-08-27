<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { setNavUser } from '../services/navAuth.js'

const router = useRouter()
const form = reactive({ username: '', password: '', confirm: '' })
const error = ref('')
const submitting = ref(false)

async function submit() {
  error.value = ''
  if (form.username.length < 2) return (error.value = '用户名至少2个字符')
  if (form.password.length < 6) return (error.value = '密码至少6个字符')
  if (form.password !== form.confirm) return (error.value = '两次输入的密码不一致')
  submitting.value = true
  const body = new FormData()
  body.append('username', form.username)
  body.append('password', form.password)
  try {
    const res = await fetch('/api/nav/register', { method: 'POST', body, credentials: 'include' })
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
      <p class="subtitle">注册导航站账号</p>
      <div v-if="error" class="alert alert-error" style="display:block">{{ error }}</div>
      <form @submit.prevent="submit">
        <div class="form-group"><label>用户名</label><input v-model.trim="form.username" required minlength="2" placeholder="至少2个字符" /></div>
        <div class="form-group"><label>密码</label><input v-model="form.password" type="password" required minlength="6" placeholder="至少6个字符" /></div>
        <div class="form-group"><label>确认密码</label><input v-model="form.confirm" type="password" required placeholder="再次输入密码" /></div>
        <button class="btn btn-primary" :disabled="submitting">{{ submitting ? '注册中…' : '注 册' }}</button>
      </form>
      <p class="auth-footer">已有账号？<RouterLink to="/nav/login">返回登录</RouterLink> · <RouterLink to="/">返回首页</RouterLink></p>
    </div>
  </main>
</template>
