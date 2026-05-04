<template>
  <div style="max-width: 900px; margin: 0 auto;">
    <a-card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 12px;">
          <span>{{ authConfig.title }}</span>
          <a-tag :color="authConfig.color">{{ authType }}</a-tag>
        </div>
      </template>

      <a-steps :current="currentStep" style="margin-bottom: 32px;">
        <a-step v-for="(step, index) in steps" :key="index" :title="step.title">
          <template #icon>
            <span style="font-size: 18px;">{{ step.icon }}</span>
          </template>
        </a-step>
      </a-steps>

      <a-row :gutter="24">
        <a-col :span="14">
          <a-card
            size="small"
            :title="steps[currentStep]?.title"
            :style="{ borderColor: authConfig.color }"
          >
            <p style="color: #666; margin-bottom: 16px;">{{ steps[currentStep]?.desc }}</p>

            <div v-if="currentStep === 0">
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="请求方法">POST</a-descriptions-item>
                <a-descriptions-item label="请求地址">{{ requestData.url }}</a-descriptions-item>
                <a-descriptions-item label="Content-Type">application/json</a-descriptions-item>
                <a-descriptions-item label="请求体">
                  <pre class="code-block">{{ requestData.body }}</pre>
                </a-descriptions-item>
              </a-descriptions>
            </div>

            <div v-if="currentStep === 1">
              <a-typography-paragraph>
                {{ steps[currentStep]?.detail }}
              </a-typography-paragraph>
              <a-alert
                v-if="authType === 'session'"
                message="Session存储在服务端数据库中，客户端只保存sessionid"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
              <a-alert
                v-if="authType === 'token'"
                message="JWT由三部分组成：Header.Payload.Signature，服务端用密钥签名"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
              <a-alert
                v-if="authType === 'cookie'"
                message="Cookie方式本质也是JWT Token，只是存储位置从localStorage换成了Cookie"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
            </div>

            <div v-if="currentStep === 2">
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="状态码">
                  <a-tag color="green">200 OK</a-tag>
                </a-descriptions-item>
                <a-descriptions-item label="响应体">
                  <pre class="code-block">{{ responseData.body }}</pre>
                </a-descriptions-item>
                <a-descriptions-item v-if="responseData.setCookie" label="Set-Cookie">
                  <pre class="code-block" style="color: #fa8c16;">{{ responseData.setCookie }}</pre>
                </a-descriptions-item>
              </a-descriptions>
            </div>

            <div v-if="currentStep === 3">
              <div v-if="authType === 'session'">
                <a-descriptions bordered :column="1" size="small">
                  <a-descriptions-item label="存储位置">
                    <a-tag color="blue">浏览器Cookie（自动）</a-tag>
                  </a-descriptions-item>
                  <a-descriptions-item label="Cookie名称">studyhub_sessionid</a-descriptions-item>
                  <a-descriptions-item label="HttpOnly">
                    <a-tag color="red">True</a-tag> <span style="color: #999; font-size: 12px;">JS无法读取，防XSS</span>
                  </a-descriptions-item>
                  <a-descriptions-item label="存储内容">
                    <pre class="code-block">{{ storeData.content }}</pre>
                  </a-descriptions-item>
                </a-descriptions>
              </div>
              <div v-if="authType === 'token'">
                <a-descriptions bordered :column="1" size="small">
                  <a-descriptions-item label="存储位置">
                    <a-tag color="green">localStorage（手动）</a-tag>
                  </a-descriptions-item>
                  <a-descriptions-item label="Key">access_token</a-descriptions-item>
                  <a-descriptions-item label="Value">
                    <pre class="code-block" style="color: #52c41a;">{{ storeData.accessToken }}</pre>
                  </a-descriptions-item>
                  <a-descriptions-item label="Key">refresh_token</a-descriptions-item>
                  <a-descriptions-item label="Value">
                    <pre class="code-block" style="color: #52c41a;">{{ storeData.refreshToken }}</pre>
                  </a-descriptions-item>
                </a-descriptions>
              </div>
              <div v-if="authType === 'cookie'">
                <a-descriptions bordered :column="1" size="small">
                  <a-descriptions-item label="存储位置">
                    <a-tag color="orange">浏览器Cookie（自动）</a-tag>
                  </a-descriptions-item>
                  <a-descriptions-item label="Cookie名称">access_token</a-descriptions-item>
                  <a-descriptions-item label="HttpOnly">
                    <a-tag color="red">True</a-tag> <span style="color: #999; font-size: 12px;">JS无法读取，防XSS</span>
                  </a-descriptions-item>
                  <a-descriptions-item label="SameSite">Lax <span style="color: #999; font-size: 12px;">防CSRF</span></a-descriptions-item>
                  <a-descriptions-item label="存储内容">
                    <pre class="code-block">{{ storeData.content }}</pre>
                  </a-descriptions-item>
                </a-descriptions>
              </div>
            </div>

            <div v-if="currentStep === 4">
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="请求方式">
                  <a-tag :color="authConfig.color">{{ requestData.method }}</a-tag>
                </a-descriptions-item>
                <a-descriptions-item v-if="authType === 'session'" label="携带方式">
                  浏览器自动携带 <pre class="code-block" style="color: #1890ff;">Cookie: studyhub_sessionid=xxx; csrftoken=yyy</pre>
                  <pre class="code-block" style="color: #1890ff; margin-top: 4px;">X-CSRFToken: yyy</pre>
                </a-descriptions-item>
                <a-descriptions-item v-if="authType === 'token'" label="携带方式">
                  手动添加请求头 <pre class="code-block" style="color: #52c41a;">Authorization: Bearer eyJhbGci...</pre>
                </a-descriptions-item>
                <a-descriptions-item v-if="authType === 'cookie'" label="携带方式">
                  浏览器自动携带 <pre class="code-block" style="color: #fa8c16;">Cookie: access_token=eyJhbGci...</pre>
                </a-descriptions-item>
                <a-descriptions-item label="服务端验证">
                  {{ steps[currentStep]?.detail }}
                </a-descriptions-item>
              </a-descriptions>
            </div>
          </a-card>
        </a-col>

        <a-col :span="10">
          <a-card size="small" title="数据流向" :bordered="false" style="background: #fafafa;">
            <div class="flow-diagram">
              <div class="flow-node" :class="{ active: currentStep === 0 }" style="background: #e6f7ff; border-color: #1890ff;">
                <span class="flow-icon">🖥️</span>
                <span>前端浏览器</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 0 }">
                {{ currentStep === 0 ? '发送请求 ➡️' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 1 }" style="background: #f6ffed; border-color: #52c41a;">
                <span class="flow-icon">⚙️</span>
                <span>服务端处理</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 2 }">
                {{ currentStep === 2 ? '⬅️ 返回响应' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 3 }" :style="{ background: authConfig.bgColor, borderColor: authConfig.color }">
                <span class="flow-icon">{{ authType === 'token' ? '💾' : '🍪' }}</span>
                <span>{{ authType === 'token' ? 'localStorage' : 'Cookie存储' }}</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 4 }">
                {{ currentStep === 4 ? '携带凭证 ➡️' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 4 }" style="background: #f6ffed; border-color: #52c41a;">
                <span class="flow-icon">✅</span>
                <span>验证通过</span>
              </div>
            </div>
          </a-card>

          <a-card size="small" title="当前状态" :bordered="false" style="background: #fafafa; margin-top: 12px;">
            <a-result
              v-if="currentStep >= 4 && loginSuccess"
              status="success"
              title="登录成功"
              :sub-title="`已通过${authConfig.title}完成认证`"
            >
              <template #extra>
                <a-button type="primary" @click="goHome">进入首页</a-button>
              </template>
            </a-result>
            <a-result
              v-else-if="loginError"
              status="error"
              title="登录失败"
              :sub-title="loginError"
            >
              <template #extra>
                <a-button type="primary" @click="goBack">返回登录</a-button>
              </template>
            </a-result>
            <div v-else style="text-align: center; padding: 20px 0;">
              <a-spin v-if="isProcessing" :tip="processingText" />
              <div v-else style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
                <a-button type="primary" @click="nextStep">
                  {{ currentStep === 0 ? '下一步：查看如何发送请求' : currentStep === 1 ? '下一步：发送请求' : currentStep === 2 ? '下一步：查看凭证存储' : currentStep === 3 ? '下一步：完成' : '完成' }}
                </a-button>
                <a-button type="link" @click="skipDemo" style="color: #999;">
                  跳过演示，直接登录
                </a-button>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../store/user'
import { sessionLogin, tokenLogin, cookieLogin } from '../api/auth'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const authType = computed(() => (route.query.type as string) || 'session')
const username = ref('')
const password = ref('')

const currentStep = ref(0)
const isProcessing = ref(false)
const loginSuccess = ref(false)
const loginError = ref('')
const loginResponse = ref<any>(null)

const processingText = computed(() => {
  if (currentStep.value === 0) return '正在发送请求...'
  if (currentStep.value === 1) return '服务端处理中...'
  return '处理中...'
})

const authConfig = computed(() => {
  const configs: Record<string, any> = {
    session: { title: '🔐 Session认证', color: '#1890ff', bgColor: '#e6f7ff' },
    token: { title: '🔑 Token(JWT)认证', color: '#52c41a', bgColor: '#f6ffed' },
    cookie: { title: '🍪 Cookie认证', color: '#fa8c16', bgColor: '#fff7e6' },
  }
  return configs[authType.value] || configs.session
})

const requestData = computed(() => {
  const urls: Record<string, string> = {
    session: '/api/auth/session/login/',
    token: '/api/auth/token/login/',
    cookie: '/api/auth/cookie/login/',
  }
  const bodies: Record<string, string> = {
    session: JSON.stringify({ username: username.value, password: '••••••' }, null, 2),
    token: JSON.stringify({ username: username.value, password: '••••••' }, null, 2),
    cookie: JSON.stringify({ username: username.value, password: '••••••' }, null, 2),
  }
  const methods: Record<string, string> = {
    session: 'Cookie自动携带',
    token: 'Authorization头手动携带',
    cookie: 'Cookie自动携带',
  }
  return { url: urls[authType.value], body: bodies[authType.value], method: methods[authType.value] }
})

const responseData = computed(() => {
  if (!loginResponse.value) return { body: '等待响应...', setCookie: '' }
  const data = loginResponse.value.data
  const body: any = { user: data.user }
  if (authType.value === 'token') {
    body.access = data.access ? data.access.substring(0, 30) + '...' : ''
    body.refresh = data.refresh ? data.refresh.substring(0, 30) + '...' : ''
  }
  const setCookies: Record<string, string> = {
    session: `studyhub_sessionid=xxxxxx; HttpOnly; SameSite=Lax; Max-Age=604800`,
    cookie: `access_token=eyJhbG...; HttpOnly; SameSite=Lax; Max-Age=3600\nrefresh_token=eyJhbG...; HttpOnly; SameSite=Lax; Max-Age=604800\nusername=${username.value}; SameSite=Lax; Max-Age=604800`,
  }
  return { body: JSON.stringify(body, null, 2), setCookie: setCookies[authType.value] || '' }
})

const storeData = computed(() => {
  if (!loginResponse.value) return { content: '', accessToken: '', refreshToken: '' }
  const data = loginResponse.value.data
  if (authType.value === 'session') {
    return { content: `sessionid: ${data.session_data?.session_key || 'xxx'}\n(实际值由Set-Cookie自动设置，JS不可读)` }
  }
  if (authType.value === 'token') {
    return {
      content: '',
      accessToken: data.access ? data.access.substring(0, 50) + '...' : '',
      refreshToken: data.refresh ? data.refresh.substring(0, 50) + '...' : '',
    }
  }
  return { content: `access_token: eyJhbG...\nrefresh_token: eyJhbG...\nusername: ${username.value}\n(由Set-Cookie自动设置，HttpOnly的Token JS不可读)` }
})

const steps = computed(() => {
  const allSteps: Record<string, any[]> = {
    session: [
      { title: '发送请求', icon: '📤', desc: '前端将用户名和密码以JSON格式发送到服务端', detail: '' },
      { title: '服务端验证', icon: '⚙️', desc: '服务端验证用户名密码，创建Session', detail: 'Django调用authenticate()验证用户名密码，验证通过后调用login()创建Session。Session数据存储在服务端数据库中，包含用户ID、过期时间等信息。同时生成唯一的sessionid作为Session的标识。' },
      { title: '返回响应', icon: '📥', desc: '服务端通过Set-Cookie返回sessionid', detail: '' },
      { title: '浏览器存储', icon: '🍪', desc: '浏览器自动保存sessionid到Cookie', detail: '' },
      { title: '后续请求', icon: '🔄', desc: '浏览器自动携带Cookie，服务端根据sessionid查找用户', detail: '服务端从Cookie中取出sessionid，在数据库中查找对应的Session记录，从中获取用户ID，加载用户对象到request.user。同时验证csrftoken（CSRF防护）：对比Cookie中的csrftoken和请求头X-CSRFToken是否匹配，防止跨站伪造请求。' },
    ],
    token: [
      { title: '发送请求', icon: '📤', desc: '前端将用户名和密码以JSON格式发送到服务端', detail: '' },
      { title: '服务端生成JWT', icon: '⚙️', desc: '服务端验证用户名密码，生成JWT Token', detail: 'Django调用authenticate()验证用户名密码，验证通过后使用SimpleJWT生成Token。access_token有效期60分钟，refresh_token有效期7天。Token中包含用户ID、过期时间等信息，使用密钥签名。' },
      { title: '返回响应', icon: '📥', desc: '服务端返回access_token和refresh_token', detail: '' },
      { title: '前端存储', icon: '💾', desc: '前端将Token存储到localStorage', detail: '' },
      { title: '后续请求', icon: '🔄', desc: '前端在Authorization头中携带Token', detail: '前端从localStorage取出access_token，添加到请求头Authorization: Bearer <token>。服务端JWTAuthentication中间件解析Token，验证签名和有效期，从Token中提取用户ID。' },
    ],
    cookie: [
      { title: '发送请求', icon: '📤', desc: '前端将用户名和密码以JSON格式发送到服务端', detail: '' },
      { title: '服务端生成JWT', icon: '⚙️', desc: '服务端验证用户名密码，生成JWT Token并通过Set-Cookie设置', detail: 'Django调用authenticate()验证用户名密码，验证通过后生成JWT Token。与Token认证不同，这里不将Token返回在响应体中，而是通过Set-Cookie响应头将Token设置到浏览器Cookie中。' },
      { title: '返回响应', icon: '📥', desc: '服务端通过Set-Cookie将Token设置到浏览器', detail: '' },
      { title: '浏览器存储', icon: '🍪', desc: '浏览器自动保存Cookie（含HttpOnly的Token）', detail: '' },
      { title: '后续请求', icon: '🔄', desc: '浏览器自动携带Cookie，服务端从Cookie中提取Token验证', detail: '浏览器自动携带Cookie中的access_token，服务端从request.COOKIES中取出Token，使用JWTAuthentication验证Token签名和有效期，从Token中提取用户信息。' },
    ],
  }
  return allSteps[authType.value] || allSteps.session
})

const sendRequest = async () => {
  isProcessing.value = true
  try {
    let response: any
    switch (authType.value) {
      case 'session':
        response = await sessionLogin({ username: username.value, password: password.value })
        break
      case 'token':
        response = await tokenLogin({ username: username.value, password: password.value })
        break
      case 'cookie':
        response = await cookieLogin({ username: username.value, password: password.value })
        break
    }
    loginResponse.value = response
    currentStep.value = 2
    isProcessing.value = false
  } catch (err: any) {
    loginError.value = err.response?.data?.error || '登录失败，请检查用户名和密码'
    isProcessing.value = false
    return
  }
}

const nextStep = () => {
  if (currentStep.value === 0) {
    currentStep.value = 1
  } else if (currentStep.value === 1) {
    sendRequest()
  } else if (currentStep.value === 2) {
    currentStep.value = 3
    const res = loginResponse.value
    if (authType.value === 'token') {
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
    }
    userStore.setUser(res.data.user, authType.value)
    sessionStorage.removeItem('login_username')
    sessionStorage.removeItem('login_password')
  } else if (currentStep.value === 3) {
    currentStep.value = 4
    loginSuccess.value = true
  }
}

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.push('/login')
}

const skipDemo = async () => {
  isProcessing.value = true
  try {
    let response: any
    switch (authType.value) {
      case 'session':
        response = await sessionLogin({ username: username.value, password: password.value })
        break
      case 'token':
        response = await tokenLogin({ username: username.value, password: password.value })
        break
      case 'cookie':
        response = await cookieLogin({ username: username.value, password: password.value })
        break
    }
    const res = response
    if (authType.value === 'token') {
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
    }
    userStore.setUser(res.data.user, authType.value)
    sessionStorage.removeItem('login_username')
    sessionStorage.removeItem('login_password')
    currentStep.value = 4
    loginSuccess.value = true
    isProcessing.value = false
  } catch (err: any) {
    loginError.value = err.response?.data?.error || '登录失败，请检查用户名和密码'
    isProcessing.value = false
  }
}

onMounted(() => {
  const storedUsername = sessionStorage.getItem('login_username')
  const storedPassword = sessionStorage.getItem('login_password')
  if (!storedUsername || !storedPassword) {
    router.push('/login')
    return
  }
  username.value = storedUsername
  password.value = storedPassword
})
</script>

<style scoped>
.code-block {
  background: #f5f5f5;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-family: 'Courier New', Courier, monospace;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.flow-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.flow-node {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #d9d9d9;
  border-radius: 8px;
  text-align: center;
  font-size: 13px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.flow-node.active {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  font-weight: 600;
}

.flow-icon {
  font-size: 18px;
}

.flow-arrow {
  font-size: 12px;
  color: #999;
  transition: all 0.3s;
  padding: 2px 0;
}

.flow-arrow.active {
  color: #1890ff;
  font-weight: 600;
}
</style>
