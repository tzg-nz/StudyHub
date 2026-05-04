<template>
  <div style="max-width: 900px; margin: 0 auto;">
    <a-card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 12px;">
          <span>{{ postData.is_draft ? '📋 保存草稿' : '📝 发布帖子' }} - 理解认证如何保护资源</span>
          <a-tag :color="authConfig.color">{{ authType }}认证</a-tag>
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
                <a-descriptions-item label="帖子标题">
                  <pre class="code-block">{{ postData.title }}</pre>
                </a-descriptions-item>
                <a-descriptions-item label="帖子内容">
                  <pre class="code-block">{{ postData.content }}</pre>
                </a-descriptions-item>
              </a-descriptions>
            </div>

            <div v-if="currentStep === 1">
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="请求方法">POST</a-descriptions-item>
                <a-descriptions-item label="请求地址">/api/posts/</a-descriptions-item>
                <a-descriptions-item label="Content-Type">application/json</a-descriptions-item>
                <a-descriptions-item label="认证方式">
                  <a-tag :color="authConfig.color">{{ authType }}</a-tag>
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
              </a-descriptions>
            </div>

            <div v-if="currentStep === 2">
              <a-typography-paragraph>
                {{ steps[currentStep]?.detail }}
              </a-typography-paragraph>
              <a-alert
                v-if="authType === 'session'"
                message="服务端从Cookie取出sessionid，查找Session获取用户身份；同时验证csrftoken与X-CSRFToken是否匹配，防止CSRF攻击"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
              <a-alert
                v-if="authType === 'token'"
                message="服务端解析Authorization头中的JWT Token，验证签名，提取用户信息"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
              <a-alert
                v-if="authType === 'cookie'"
                message="服务端从Cookie中取出access_token，使用JWTAuthentication验证Token"
                type="info"
                show-icon
                style="margin-top: 12px;"
              />
            </div>

            <div v-if="currentStep === 3">
              <a-descriptions bordered :column="1" size="small">
                <a-descriptions-item label="状态码">
                  <a-tag color="green">201 Created</a-tag>
                </a-descriptions-item>
                <a-descriptions-item label="响应体">
                  <pre class="code-block">{{ responseData.body }}</pre>
                </a-descriptions-item>
              </a-descriptions>
            </div>

            <div v-if="currentStep === 4">
              <a-typography-paragraph>
                {{ steps[currentStep]?.detail }}
              </a-typography-paragraph>
              <a-result
                status="success"
                :title="`${postData.is_draft ? '草稿已保存' : '帖子已发布'}，认证方式：${authConfig.title}`"
                :sub-title="postData.is_draft ? '认证机制确保只有登录用户才能保存内容' : '不同的认证方式都能让服务端识别用户身份，从而保护写操作'"
              />
            </div>
          </a-card>
        </a-col>

        <a-col :span="10">
          <a-card size="small" title="数据流向" :bordered="false" style="background: #fafafa;">
            <div class="flow-diagram">
              <div class="flow-node" :class="{ active: currentStep === 0 }" style="background: #e6f7ff; border-color: #1890ff;">
                <span class="flow-icon">📝</span>
                <span>输入帖子内容</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 1 }">
                {{ currentStep === 1 ? '携带凭证发送 ➡️' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 1 }" :style="{ background: authConfig.bgColor, borderColor: authConfig.color }">
                <span class="flow-icon">{{ authType === 'token' ? '🔑' : '🍪' }}</span>
                <span>携带{{ authType === 'token' ? 'Token' : 'Cookie' }}</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 2 }">
                {{ currentStep === 2 ? '⬇️' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 2 }" style="background: #f6ffed; border-color: #52c41a;">
                <span class="flow-icon">🔒</span>
                <span>服务端验证身份</span>
              </div>
              <div class="flow-arrow" :class="{ active: currentStep === 3 }">
                {{ currentStep === 3 ? '⬅️ 返回结果' : '⬇️' }}
              </div>
              <div class="flow-node" :class="{ active: currentStep === 4 }" style="background: #f6ffed; border-color: #52c41a;">
                <span class="flow-icon">✅</span>
                <span>{{ postData.is_draft ? '保存成功' : '发布成功' }}</span>
              </div>
            </div>
          </a-card>

          <a-card size="small" title="当前状态" :bordered="false" style="background: #fafafa; margin-top: 12px;">
            <a-result
              v-if="currentStep >= 4 && postSuccess"
              status="success"
              :title="postData.is_draft ? '草稿保存成功' : '帖子发布成功'"
              :sub-title="`已通过${authConfig.title}完成认证并${postData.is_draft ? '保存草稿' : '发布帖子'}`"
            >
              <template #extra>
                <a-button type="primary" @click="goHome">返回首页</a-button>
              </template>
            </a-result>
            <a-result
              v-else-if="postError"
              status="error"
              :title="postData.is_draft ? '保存失败' : '发布失败'"
              :sub-title="postError"
            >
              <template #extra>
                <a-button type="primary" @click="goBack">返回首页</a-button>
              </template>
            </a-result>
            <div v-else style="text-align: center; padding: 20px 0;">
              <a-spin v-if="isProcessing" :tip="processingText" />
              <div v-else style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
                <a-button type="primary" @click="nextStep">
                  {{ currentStep === 0 ? '下一步：查看如何携带凭证' : currentStep === 1 ? '下一步：发送请求' : currentStep === 2 ? '下一步：查看结果' : currentStep === 3 ? '下一步：完成' : '完成' }}
                </a-button>
                <a-button type="link" @click="skipDemo" style="color: #999;">
                  跳过演示，直接{{ postData.is_draft ? '保存' : '发布' }}
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
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { createPost } from '../api/posts'

const router = useRouter()
const userStore = useUserStore()

const authType = computed(() => userStore.authType || 'session')
const postData = ref({ title: '', content: '', is_draft: false })

const currentStep = ref(0)
const isProcessing = ref(false)
const postSuccess = ref(false)
const postError = ref('')
const postResponse = ref<any>(null)
const hasRequested = ref(false)

const processingText = computed(() => {
  if (currentStep.value === 1) return '正在发送请求...'
  if (currentStep.value === 2) return '服务端处理中...'
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

const responseData = computed(() => {
  if (!postResponse.value) return { body: '等待响应...' }
  const data = postResponse.value.data
  return { body: JSON.stringify(data, null, 2) }
})

const steps = computed(() => {
  const isDraft = postData.value.is_draft
  return [
    { title: isDraft ? '填写内容' : '填写内容', icon: '📝', desc: isDraft ? '用户输入帖子标题，内容可稍后补充' : '用户在弹窗中输入帖子标题和内容', detail: '' },
    { title: '携带凭证', icon: '📤', desc: '查看前端如何携带认证凭证发送请求', detail: '' },
    { title: '服务端验证', icon: '🔒', desc: '查看服务端如何验证用户身份', detail: `服务端通过${authType.value === 'session' ? 'SessionAuthentication从Cookie中获取sessionid识别用户身份，并验证csrftoken防止CSRF攻击' : authType.value === 'token' ? 'JWTAuthentication从Authorization头中获取Token' : '从Cookie中获取access_token'}验证用户身份，确认用户已登录后才允许操作` },
    { title: '返回结果', icon: '📥', desc: isDraft ? '服务端保存草稿，返回201 Created' : '服务端创建帖子，返回201 Created', detail: '' },
    { title: isDraft ? '保存成功' : '发布成功', icon: '✅', desc: isDraft ? '草稿保存成功' : '帖子发布成功', detail: isDraft ? '草稿已保存，你可以稍后在"我的草稿"中继续编辑并发布。认证机制确保只有登录用户才能保存内容。' : '无论使用哪种认证方式，服务端都能正确识别用户身份。这就是认证的作用：保护需要登录才能操作的资源。' },
  ]
})

const sendRequest = async () => {
  isProcessing.value = true
  try {
    const response = await createPost(postData.value)
    postResponse.value = response
    hasRequested.value = true
    isProcessing.value = false
    currentStep.value = 2
  } catch (err: any) {
    postError.value = err.response?.data?.error || (postData.value.is_draft ? '保存失败，请检查是否已登录' : '发布失败，请检查是否已登录')
    isProcessing.value = false
    return
  }
}

const nextStep = () => {
  if (currentStep.value === 1) {
    sendRequest()
  } else if (currentStep.value === 4) {
    currentStep.value = 4
    postSuccess.value = true
  } else {
    currentStep.value += 1
    if (currentStep.value === 4) {
      postSuccess.value = true
    }
  }
}

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.push('/')
}

const skipDemo = async () => {
  isProcessing.value = true
  try {
    const response = await createPost(postData.value)
    postResponse.value = response
    postSuccess.value = true
    isProcessing.value = false
    currentStep.value = 4
    sessionStorage.removeItem('post_title')
    sessionStorage.removeItem('post_content')
    sessionStorage.removeItem('post_is_draft')
  } catch (err: any) {
    postError.value = err.response?.data?.error || (postData.value.is_draft ? '保存失败，请检查是否已登录' : '发布失败，请检查是否已登录')
    isProcessing.value = false
  }
}

onMounted(() => {
  const storedTitle = sessionStorage.getItem('post_title')
  const storedContent = sessionStorage.getItem('post_content')
  const storedIsDraft = sessionStorage.getItem('post_is_draft') === 'true'
  if (!storedTitle) {
    router.push('/')
    return
  }
  postData.value = { title: storedTitle, content: storedContent || '', is_draft: storedIsDraft }
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
