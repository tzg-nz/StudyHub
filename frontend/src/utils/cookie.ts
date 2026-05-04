/**
 * Cookie工具函数 - 用于读取浏览器Cookie
 */

/**
 * 获取指定名称的Cookie值
 */
export function getCookie(name: string): string {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    const cookieValue = parts.pop()?.split(';').shift()
    return cookieValue || ''
  }
  return ''
}

/**
 * 获取所有Cookie
 */
export function getAllCookies(): Record<string, string> {
  const cookies: Record<string, string> = {}
  if (document.cookie) {
    document.cookie.split(';').forEach((cookie) => {
      const [name, value] = cookie.trim().split('=')
      if (name && value) {
        cookies[name] = value
      }
    })
  }
  return cookies
}

/**
 * 获取CSRF Token
 * Django默认的CSRF cookie名称是csrftoken
 */
export function getCSRFToken(): string {
  return getCookie('csrftoken')
}
