<template>
  <div style="max-width: 1200px; margin: 0 auto;">
    <a-row :gutter="24">
      <a-col :span="16">
        <a-card :bordered="false">
          <template #title>
            <div style="display: flex; align-items: center; gap: 12px;">
              <span>最新帖子</span>
              <a-input-search
                v-model:value="searchText"
                placeholder="搜索帖子..."
                style="width: 240px;"
                @search="handleSearch"
                allow-clear
              />
            </div>
          </template>
          <template #extra>
            <a-button type="primary" @click="showCreateModal = true" v-if="userStore.isLoggedIn">
              发布帖子
            </a-button>
          </template>
          <a-list :data-source="posts" :loading="loading">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <router-link :to="`/posts/${item.id}`" style="font-size: 16px;">
                        {{ item.title }}
                      </router-link>
                      <a-tag v-if="item.is_draft" color="default">草稿</a-tag>
                    </div>
                  </template>
                  <template #description>
                    <div style="display: flex; align-items: center; gap: 16px; color: #999;">
                      <span>{{ item.author_name }}</span>
                      <span>{{ formatTime(item.created_at) }}</span>
                    </div>
                  </template>
                </a-list-item-meta>
                <template #actions>
                  <span style="color: #999; font-size: 13px;">
                    👁️ {{ item.views }} &nbsp;
                    ❤️ {{ item.like_count }} &nbsp;
                    ⭐ {{ item.favorite_count }} &nbsp;
                    💬 {{ item.comment_count }}
                  </span>
                </template>
              </a-list-item>
            </template>
            <template #footer>
              <div style="text-align: center; padding: 12px 0;">
                <a-pagination
                  v-model:current="currentPage"
                  :total="totalPosts"
                  :pageSize="pageSize"
                  @change="handlePageChange"
                  show-less-items
                />
              </div>
            </template>
            <template #empty>
              <a-empty description="暂无帖子" />
            </template>
          </a-list>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="认证机制学习" :bordered="false" style="margin-bottom: 16px;">
          <p>本项目演示三种Web认证机制：</p>
          <a-space direction="vertical" style="width: 100%;">
            <a-tag color="blue">Session - 服务端存储</a-tag>
            <a-tag color="green">Token(JWT) - 客户端存储</a-tag>
            <a-tag color="orange">Cookie - 浏览器存储</a-tag>
          </a-space>
          <a-divider />
          <a-space direction="vertical" style="width: 100%;">
            <a-button type="link" @click="$router.push('/auth-security')" block>
              🛡️ 认证安全对比与攻击演示 →
            </a-button>
          </a-space>
        </a-card>
        <a-card v-if="userStore.isLoggedIn" title="我的内容" :bordered="false" style="margin-bottom: 16px;">
          <a-space direction="vertical" style="width: 100%;">
            <a-button type="link" @click="$router.push('/my/posts')" block>📝 我的帖子</a-button>
            <a-button type="link" @click="$router.push('/my/favorites')" block>⭐ 我的收藏</a-button>
            <a-button type="link" @click="$router.push('/my/drafts')" block>📋 我的草稿</a-button>
          </a-space>
        </a-card>
        <a-card v-else title="快速入口" :bordered="false">
          <a-space direction="vertical" style="width: 100%;">
            <a-button type="primary" block @click="$router.push('/login')">登录体验三种认证</a-button>
            <a-button block @click="$router.push('/register')">注册新账号</a-button>
          </a-space>
        </a-card>
      </a-col>
    </a-row>

    <a-modal v-model:open="showCreateModal" title="发布新帖子" :footer="null" width="600px">
      <a-space direction="vertical" style="width: 100%;" :size="12">
        <a-input v-model:value="postForm.title" placeholder="请输入帖子标题" />
        <a-textarea v-model:value="postForm.content" :rows="8" placeholder="请输入帖子内容" />
        <div style="display: flex; gap: 8px; justify-content: flex-end;">
          <a-button @click="handleSaveDraft">保存草稿</a-button>
          <a-button type="primary" @click="handlePublish">发布</a-button>
        </div>
      </a-space>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { getPostList } from '../api/posts'

const router = useRouter()
const userStore = useUserStore()
const posts = ref<any[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const postForm = ref({ title: '', content: '', is_draft: false })
const searchText = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPosts = ref(0)

const formatTime = (time: string) => {
  if (!time) return ''
  const d = new Date(time)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

const fetchPosts = async () => {
  loading.value = true
  try {
    const params: any = { page: currentPage.value }
    if (searchText.value) params.search = searchText.value
    const res = await getPostList(params)
    posts.value = res.data.results || res.data
    totalPosts.value = res.data.count || posts.value.length
  } catch {
    message.error('获取帖子列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchPosts()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchPosts()
}

const handleSaveDraft = () => {
  if (!postForm.value.title) {
    message.warning('请填写标题')
    return
  }
  sessionStorage.setItem('post_title', postForm.value.title)
  sessionStorage.setItem('post_content', postForm.value.content || '')
  sessionStorage.setItem('post_is_draft', 'true')
  showCreateModal.value = false
  postForm.value = { title: '', content: '', is_draft: false }
  router.push('/post-process')
}

const handlePublish = () => {
  if (!postForm.value.title) {
    message.warning('请填写标题')
    return
  }
  if (!postForm.value.content) {
    message.warning('发布帖子请填写内容，或选择保存草稿')
    return
  }
  sessionStorage.setItem('post_title', postForm.value.title)
  sessionStorage.setItem('post_content', postForm.value.content)
  sessionStorage.setItem('post_is_draft', 'false')
  showCreateModal.value = false
  postForm.value = { title: '', content: '', is_draft: false }
  router.push('/post-process')
}

onMounted(() => {
  fetchPosts()
  userStore.restoreFromStorage()
})
</script>
