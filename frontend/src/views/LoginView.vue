<template>
  <div style="max-width: 500px; margin: 40px auto;">
    <a-card title="登录 - 体验三种认证方式">
      <template #extra>
        <router-link to="/register">没有账号？去注册</router-link>
      </template>

      <a-alert
        message="三种认证方式说明"
        description="Session：服务端存储会话；Token：客户端存储令牌；Cookie：浏览器存储令牌。选择不同方式登录，体验它们的差异。"
        type="info"
        show-icon
        style="margin-bottom: 16px;"
      />

      <a-space direction="vertical" style="width: 100%;" :size="16">
        <a-input v-model:value="username" placeholder="请输入用户名" allow-clear />
        <a-input-password v-model:value="password" placeholder="请输入密码" />
        <a-alert v-if="username || password" :message="`用户名: ${username}, 密码: ${password ? '***' : '(空)'}`" type="info" />

        <a-divider>选择认证方式</a-divider>

        <a-space direction="vertical" style="width: 100%;" :size="12">
          <a-button type="primary" block @click="handleLogin('session')">
            🔐 Session认证登录
          </a-button>
          <a-button block style="color: #52c41a; border-color: #52c41a;" @click="handleLogin('token')">
            🔑 Token(JWT)认证登录
          </a-button>
          <a-button block style="color: #fa8c16; border-color: #fa8c16;" @click="handleLogin('cookie')">
            🍪 Cookie认证登录
          </a-button>
        </a-space>
      </a-space>

      <a-divider />

      <a-collapse ghost>
        <a-collapse-panel key="1" header="💡 三种认证方式有什么区别？">
          <a-typography-paragraph>
            <strong>Session认证：</strong>服务端存储会话数据，通过sessionid Cookie标识用户。登录后浏览器自动携带sessionid，服务端据此查找用户信息。
          </a-typography-paragraph>
          <a-typography-paragraph>
            <strong>Token认证：</strong>服务端生成加密令牌(JWT)，客户端存储在localStorage。每次请求手动在Authorization头中携带Token，服务端验证Token签名即可识别用户。
          </a-typography-paragraph>
          <a-typography-paragraph>
            <strong>Cookie认证：</strong>将Token存储在Cookie中，浏览器自动携带。兼具Token的无状态和Cookie的自动管理特性，可设置HttpOnly防止XSS攻击。
          </a-typography-paragraph>
        </a-collapse-panel>
      </a-collapse>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = (type: 'session' | 'token' | 'cookie') => {
  if (!username.value || !password.value) {
    message.warning('请输入用户名和密码')
    return
  }
  sessionStorage.setItem('login_username', username.value)
  sessionStorage.setItem('login_password', password.value)
  router.push({ path: '/auth-process', query: { type } })
}
</script>
