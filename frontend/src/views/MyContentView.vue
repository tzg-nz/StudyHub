<template>
  <div style="max-width: 900px; margin: 0 auto;">
    <a-page-header :title="pageTitle" @back="$router.push('/')" />
    <a-input-search
      v-if="type === 'posts'"
      v-model:value="searchText"
      placeholder="搜索我的帖子..."
      style="width: 300px; margin-bottom: 16px;"
      @search="fetchData"
      allow-clear
    />
    <a-list :data-source="posts" :loading="loading">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-list-item-meta>
            <template #title>
              <div style="display: flex; align-items: center; gap: 8px;">
                <router-link :to="`/posts/${item.id}?from=my`" style="font-size: 16px;">
                  {{ item.title }}
                </router-link>
                <a-tag v-if="item.is_draft" color="default">草稿</a-tag>
              </div>
            </template>
            <template #description>
              <div style="display: flex; align-items: center; gap: 16px; color: #999;">
                <span>{{ formatTime(item.created_at) }}</span>
                <span>👁️ {{ item.views }}</span>
                <span>❤️ {{ item.like_count }}</span>
                <span>💬 {{ item.comment_count }}</span>
              </div>
            </template>
          </a-list-item-meta>
          <template #actions v-if="type === 'posts' || type === 'drafts'">
            <a-button type="link" @click="handleEdit(item)">编辑</a-button>
            <a-popconfirm title="确定删除？" @confirm="handleDelete(item)" ok-text="确定" cancel-text="取消">
              <a-button type="link" danger>删除</a-button>
            </a-popconfirm>
          </template>
          <template #actions v-else>
            <a-button type="link" @click="handleUnfavorite(item)">取消收藏</a-button>
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
        <a-empty :description="emptyText" />
      </template>
    </a-list>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { getMyPosts, getMyFavorites, getMyDrafts, deletePost, favoritePost } from '../api/posts'

const route = useRoute()
const router = useRouter()
const type = computed(() => (route.params.type as string) || 'posts')
const posts = ref<any[]>([])
const loading = ref(false)
const searchText = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPosts = ref(0)

const pageTitle = computed(() => {
  const titles: Record<string, string> = { posts: '📝 我的帖子', favorites: '⭐ 我的收藏', drafts: '📋 我的草稿' }
  return titles[type.value] || '我的内容'
})

const emptyText = computed(() => {
  const texts: Record<string, string> = { posts: '还没有发布过帖子', favorites: '还没有收藏过帖子', drafts: '还没有草稿' }
  return texts[type.value] || '暂无内容'
})

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

const fetchData = async () => {
  loading.value = true
  try {
    const params: any = { page: currentPage.value }
    if (searchText.value) params.search = searchText.value
    let res
    if (type.value === 'posts') res = await getMyPosts(params)
    else if (type.value === 'favorites') res = await getMyFavorites(params)
    else res = await getMyDrafts(params)
    posts.value = res.data.results || res.data
    totalPosts.value = res.data.count || posts.value.length
  } catch { message.error('获取数据失败') }
  finally { loading.value = false }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchData()
}

const handleEdit = (item: any) => {
  router.push(`/posts/${item.id}?from=my`)
}

const handleDelete = async (item: any) => {
  try {
    await deletePost(item.id)
    message.success('已删除')
    fetchData()
  } catch { message.error('删除失败') }
}

const handleUnfavorite = async (item: any) => {
  try {
    await favoritePost(item.id)
    message.success('已取消收藏')
    fetchData()
  } catch { message.error('操作失败') }
}

watch(type, () => { currentPage.value = 1; fetchData() })
onMounted(() => { fetchData() })
</script>
