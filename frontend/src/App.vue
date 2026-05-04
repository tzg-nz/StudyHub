<template>
  <a-config-provider :locale="zhCN">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="display: flex; align-items: center; justify-content: space-between; padding: 0 24px;">
        <div style="display: flex; align-items: center;">
          <h2 style="color: white; margin: 0; cursor: pointer;" @click="$router.push('/')">StudyHub</h2>
          <a-tag color="blue" style="margin-left: 12px;">学习认证机制</a-tag>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          <template v-if="userStore.isLoggedIn">
            <a-tag :color="authTagColor">{{ userStore.authType }}认证</a-tag>
            <span style="color: white;">{{ userStore.username }}</span>
            <a-button type="link" @click="$router.push('/profile')" style="color: white;">个人中心</a-button>
            <a-button type="link" @click="handleLogout" style="color: #ff4d4f;">退出</a-button>
          </template>
          <template v-else>
            <a-button type="primary" @click="$router.push('/login')">登录</a-button>
            <a-button @click="$router.push('/register')">注册</a-button>
          </template>
        </div>
      </a-layout-header>
      <a-layout-content style="padding: 24px;">
        <router-view />
      </a-layout-content>
      <a-layout-footer style="text-align: center;">
        StudyHub ©2026 - 学习Token/Cookie/Session认证机制
      </a-layout-footer>
    </a-layout>
  </a-config-provider>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import { useUserStore } from './store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const authTagColor = computed(() => {
  switch (userStore.authType) {
    case 'session': return 'blue'
    case 'token': return 'green'
    case 'cookie': return 'orange'
    default: return 'default'
  }
})

// 页面加载时恢复用户登录状态
onMounted(() => {
  userStore.restoreFromStorage()
})

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
