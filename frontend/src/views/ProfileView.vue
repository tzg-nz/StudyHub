<template>
  <div style="max-width: 800px; margin: 0 auto;">
    <a-card title="个人中心">
      <a-descriptions bordered :column="1">
        <a-descriptions-item label="用户名">{{ userStore.username }}</a-descriptions-item>
        <a-descriptions-item label="邮箱">{{ userStore.email || '未设置' }}</a-descriptions-item>
        <a-descriptions-item label="当前认证方式">
          <a-tag :color="authColor">{{ userStore.authType }}</a-tag>
        </a-descriptions-item>
      </a-descriptions>

      <a-divider />

      <h3>认证信息详情</h3>
      <a-row :gutter="16">
        <a-col :span="8">
          <a-card size="small" title="Session" :bordered="false" style="background: #e6f7ff;">
            <p style="font-size: 12px;">服务端存储会话</p>
            <p style="font-size: 12px;">sessionid: {{ hasSessionId ? '✅ 存在' : '❌ 无' }}</p>
            <a-button size="small" type="primary" @click="checkSession">检查Session</a-button>
          </a-card>
        </a-col>
        <a-col :span="8">
          <a-card size="small" title="Token" :bordered="false" style="background: #f6ffed;">
            <p style="font-size: 12px;">客户端存储令牌</p>
            <p style="font-size: 12px;">access_token: {{ hasToken ? '✅ 存在' : '❌ 无' }}</p>
            <a-button size="small" style="color: #52c41a; border-color: #52c41a;" @click="checkToken">检查Token</a-button>
          </a-card>
        </a-col>
        <a-col :span="8">
          <a-card size="small" title="Cookie" :bordered="false" style="background: #fff7e6;">
            <p style="font-size: 12px;">浏览器存储令牌</p>
            <p style="font-size: 12px;">Cookie中的Token: {{ hasCookieToken ? '✅ 存在' : '❌ 无' }}</p>
            <a-button size="small" style="color: #fa8c16; border-color: #fa8c16;" @click="checkCookie">检查Cookie</a-button>
          </a-card>
        </a-col>
      </a-row>

      <a-divider />

      <h3>认证检测结果</h3>
      <a-card size="small" v-if="authResult">
        <pre style="white-space: pre-wrap; font-size: 12px; background: #f5f5f5; padding: 12px; border-radius: 4px;">{{ JSON.stringify(authResult, null, 2) }}</pre>
      </a-card>
      <a-empty v-else description="点击上方按钮检测认证状态" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { message } from 'ant-design-vue'
import { useUserStore } from '../store/user'
import { getSessionProfile, getTokenProfile, getCookieProfile } from '../api/auth'

const userStore = useUserStore()
const authResult = ref<any>(null)

const authColor = computed(() => {
  switch (userStore.authType) {
    case 'session': return 'blue'
    case 'token': return 'green'
    case 'cookie': return 'orange'
    default: return 'default'
  }
})

const tokenInfo = ref({ access: '', refresh: '' })

// 根据实际认证状态判断
const hasSessionId = computed(() => {
  return userStore.authType === 'session'
})

const hasToken = computed(() => {
  return userStore.authType === 'token'
})

const hasCookieToken = computed(() => {
  return userStore.authType === 'cookie'
})

const checkSession = async () => {
  try {
    const res = await getSessionProfile()
    authResult.value = res.data
    message.success('Session认证有效')
  } catch {
    authResult.value = { error: 'Session认证失败，可能未通过Session方式登录' }
    message.warning('Session认证无效')
  }
}

const checkToken = async () => {
  try {
    const res = await getTokenProfile()
    authResult.value = res.data
    message.success('Token认证有效')
  } catch {
    authResult.value = { error: 'Token认证失败，可能Token已过期或未通过Token方式登录' }
    message.warning('Token认证无效')
  }
}

const checkCookie = async () => {
  try {
    const res = await getCookieProfile()
    authResult.value = res.data
    message.success('Cookie认证有效')
  } catch {
    authResult.value = { error: 'Cookie认证失败，可能Cookie已过期或未通过Cookie方式登录' }
    message.warning('Cookie认证无效')
  }
}

// 监听认证方式变化，实时更新状态
watch(() => userStore.authType, () => {
  authResult.value = null
})

onMounted(() => {
  tokenInfo.value.access = localStorage.getItem('access_token') || ''
  tokenInfo.value.refresh = localStorage.getItem('refresh_token') || ''
})
</script>
