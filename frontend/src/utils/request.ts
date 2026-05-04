/**
 * Axios请求封装 - 演示三种认证方式在HTTP请求中的差异
 * 
 * 【三种认证方式在请求中的体现】：
 * 1. Session认证：浏览器自动携带sessionid Cookie，无需手动处理
 * 2. Token认证：手动从localStorage取出Token，添加到Authorization头
 * 3. Cookie认证：浏览器自动携带Cookie中的Token，无需手动处理
 *    （但服务端设置Cookie时需要withCredentials=true才能跨域携带）
 */
import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { getCSRFToken } from './cookie'

const API_BASE = '/api'

/**
 * 创建Axios实例 - 基础配置
 */
const http: AxiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  /**
   * withCredentials: true
   * 【重要】跨域请求时携带Cookie
   * - Session认证需要此选项，浏览器才会发送sessionid Cookie
   * - Cookie认证需要此选项，浏览器才会发送Cookie中的Token
   * - Token认证不需要此选项，Token通过Authorization头发送
   */
  withCredentials: true,
})

/**
 * 请求拦截器 - 在请求发送前添加认证信息
 * 
 * 【Token认证的核心】：从localStorage取出Token，添加到Authorization头
 * 【Session/Cookie认证】：浏览器自动携带Cookie，无需手动处理
 * 【CSRF保护】：从Cookie中取出CSRF token，添加到请求头
 */
http.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Token认证：从localStorage获取access_token，添加到Authorization头
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // CSRF保护：添加CSRF token到请求头
    const csrfToken = getCSRFToken()
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器 - 处理Token过期等异常
 * 
 * 【Token过期的处理】：
 * - access_token过期后，使用refresh_token获取新的access_token
 * - 这就是JWT的"双Token"机制：access_token短期有效，refresh_token长期有效
 * - Session认证不存在此问题，服务端控制Session有效期
 * - Cookie认证由服务端刷新Cookie
 */
http.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Token过期（401），尝试用refresh_token刷新
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE}/auth/token/refresh/`, {
            refresh: refreshToken,
          })
          const newAccessToken = response.data.access
          localStorage.setItem('access_token', newAccessToken)
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          return http(originalRequest)
        } catch {
          // refresh_token也过期了，需要重新登录
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

export default http
