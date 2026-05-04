/**
 * 应用入口文件 - 初始化Vue3应用
 * 引入Ant Design Vue组件库、路由、状态管理
 */
import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import 'ant-design-vue/dist/reset.css'
import { getCSRFToken } from './api/auth'

const app = createApp(App)
app.use(Antd)
app.use(router)
app.use(createPinia())

// 应用启动时获取CSRF Token
getCSRFToken().then(() => {
  console.log('CSRF token已获取')
}).catch((err) => {
  console.warn('获取CSRF token失败:', err)
})

app.mount('#app')
