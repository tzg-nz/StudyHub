/**
 * 认证API - 封装三种认证方式的后端接口调用
 * 
 * 【三种认证方式调用差异】：
 * 1. Session登录：调用后login后，浏览器自动保存sessionid Cookie
 * 2. Token登录：调用后需手动将Token存到localStorage
 * 3. Cookie登录：调用后服务端通过Set-Cookie设置Token，浏览器自动保存
 */
import http from '../utils/request'

/**
 * 获取CSRF Token
 */
export function getCSRFToken() {
  return http.get('/auth/csrf/')
}

/**
 * 用户注册
 */
export function register(data: { username: string; email: string; password: string; password_confirm: string }) {
  return http.post('/auth/register/', data)
}

/**
 * Session认证登录
 * 【Session认证流程】：
 * 1. 发送用户名密码到后端
 * 2. 后端验证后创建Session，通过Set-Cookie返回sessionid
 * 3. 浏览器自动保存sessionid Cookie
 * 4. 后续请求浏览器自动携带sessionid
 */
export function sessionLogin(data: { username: string; password: string }) {
  return http.post('/auth/session/login/', data)
}

/**
 * Session认证登出
 */
export function sessionLogout() {
  return http.post('/auth/session/logout/')
}

/**
 * Session认证获取用户信息
 */
export function getSessionProfile() {
  return http.get('/auth/session/profile/')
}

/**
 * Token(JWT)认证登录
 * 【Token认证流程】：
 * 1. 发送用户名密码到后端
 * 2. 后端返回access_token和refresh_token
 * 3. 前端将Token存储到localStorage
 * 4. 后续请求在Authorization头中携带Token
 */
export function tokenLogin(data: { username: string; password: string }) {
  return http.post('/auth/token/login/', data)
}

/**
 * Token认证获取用户信息
 */
export function getTokenProfile() {
  return http.get('/auth/token/profile/')
}

/**
 * Cookie认证登录
 * 【Cookie认证流程】：
 * 1. 发送用户名密码到后端
 * 2. 后端通过Set-Cookie将Token设置到浏览器
 * 3. 浏览器自动保存并携带Cookie
 * 4. 后续请求浏览器自动携带Cookie中的Token
 */
export function cookieLogin(data: { username: string; password: string }) {
  return http.post('/auth/cookie/login/', data)
}

/**
 * Cookie认证登出
 */
export function cookieLogout() {
  return http.post('/auth/cookie/logout/')
}

/**
 * Cookie认证获取用户信息
 */
export function getCookieProfile() {
  return http.get('/auth/cookie/profile/')
}

/**
 * 三种认证方式对比
 */
export function getAuthCompare() {
  return http.get('/auth/compare/')
}
