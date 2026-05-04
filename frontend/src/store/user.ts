/**
 * 用户状态管理 - Pinia Store
 * 
 * 【三种认证方式在前端的存储差异】：
 * - Session：无需前端存储，浏览器自动通过Cookie传递sessionid
 * - Token：前端存储在localStorage，请求时手动添加到Authorization头
 * - Cookie：Token由服务端设置到Cookie，浏览器自动携带，前端无需手动处理
 * 
 * 【切换认证方式】：每次登录会清除其他认证方式的所有数据
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const userId = ref<number | null>(null)
  const username = ref('')
  const email = ref('')
  const authType = ref<string>('未登录')

  const isLoggedIn = computed(() => !!userId.value)

  /**
   * 设置用户信息 - 登录成功后调用
   * 设置新认证方式前，先清除所有旧认证数据
   * @param data 用户数据
   * @param type 认证类型：session / token / cookie
   */
  function setUser(data: { id: number; username: string; email?: string }, type: string) {
    // 清除所有旧的认证数据（Token认证的token由外部管理，不在这里清除）
    if (type !== 'token') {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }

    // 设置新的认证数据
    userId.value = data.id
    username.value = data.username
    email.value = data.email || ''
    authType.value = type
    localStorage.setItem('user_id', String(data.id))
    localStorage.setItem('username', data.username)
    localStorage.setItem('auth_type', type)
    if (data.email) {
      localStorage.setItem('email', data.email)
    }
  }

  /**
   * 登出 - 清除所有认证信息
   * 【三种认证方式清除差异】：
   * - Session：调用后端logout接口，销毁服务端Session
   * - Token：清除localStorage中的Token
   * - Cookie：调用后端logout接口，服务端设置Cookie过期
   */
  function logout() {
    userId.value = null
    username.value = ''
    email.value = ''
    authType.value = '未登录'
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('auth_type')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
    localStorage.removeItem('email')
  }

  /**
   * 从localStorage恢复登录状态
   * 页面刷新后，Token认证需要从localStorage恢复
   * Session和Cookie认证不需要，浏览器会自动携带
   */
  function restoreFromStorage() {
    const storedUserId = localStorage.getItem('user_id')
    const storedUsername = localStorage.getItem('username')
    const storedAuthType = localStorage.getItem('auth_type')
    const storedEmail = localStorage.getItem('email')
    if (storedUserId && storedUsername && storedAuthType) {
      userId.value = Number(storedUserId)
      username.value = storedUsername
      authType.value = storedAuthType
      email.value = storedEmail || ''
    }
  }

  return { userId, username, email, authType, isLoggedIn, setUser, logout, restoreFromStorage }
})
