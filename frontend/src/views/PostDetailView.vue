<template>
  <div style="max-width: 800px; margin: 0 auto;">
    <a-page-header :title="post?.title" @back="$router.back()">
      <template #extra>
        <a-tag color="blue">{{ post?.author_name }}</a-tag>
        <span style="color: #999;">{{ formatTime(post?.created_at) }}</span>
      </template>
    </a-page-header>

    <a-card :bordered="false">
      <div style="white-space: pre-wrap; line-height: 1.8;">{{ post?.content }}</div>

      <a-divider />

      <div style="display: flex; align-items: center; justify-content: space-between;">
        <template v-if="post?.is_draft">
          <a-tag color="default">📋 草稿 - 未发布</a-tag>
        </template>
        <template v-else>
          <a-space :size="16">
            <a-button type="text" :style="{ color: post?.is_liked ? '#ff4d4f' : '#999' }" @click="handleLike">
              {{ post?.is_liked ? '❤️' : '🤍' }} {{ post?.like_count || 0 }}
            </a-button>
            <a-button type="text" :style="{ color: post?.is_favorited ? '#faad14' : '#999' }" @click="handleFavorite">
              {{ post?.is_favorited ? '⭐' : '☆' }} {{ post?.favorite_count || 0 }}
            </a-button>
            <span style="color: #999;">👁️ {{ post?.views || 0 }}</span>
            <span style="color: #999;">💬 {{ post?.comment_count || 0 }}</span>
          </a-space>
        </template>
        <a-space v-if="isAuthor && isFromMy">
          <a-button type="text" @click="showEditModal = true">✏️ 编辑</a-button>
          <a-popconfirm title="确定删除这篇帖子？" @confirm="handleDelete" ok-text="确定" cancel-text="取消">
            <a-button type="text" danger>🗑️ 删除</a-button>
          </a-popconfirm>
          <a-button type="text" @click="handleShare" v-if="!post?.is_draft">🔗 分享</a-button>
        </a-space>
        <a-space v-else-if="userStore.isLoggedIn && !post?.is_draft">
          <a-button type="text" @click="handleShare">🔗 分享</a-button>
        </a-space>
      </div>

      <a-divider />

      <template v-if="post?.is_draft">
        <a-alert message="这是一篇草稿，发布后才能被其他人看到" type="info" show-icon />
      </template>
      <template v-else>
        <h3>评论 ({{ post?.comments?.length || 0 }})</h3>
      <a-list :data-source="post?.comments || []" item-layout="horizontal">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta>
              <template #title>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span>{{ item.author_name }}</span>
                  <span style="color: #999; font-size: 12px; font-weight: normal;">{{ formatTime(item.created_at) }}</span>
                </div>
              </template>
              <template #description>
                <div v-if="editingCommentId === item.id">
                  <a-textarea v-model:value="editCommentContent" :rows="2" />
                  <div style="margin-top: 8px; display: flex; gap: 8px;">
                    <a-button size="small" type="primary" @click="handleUpdateComment(item)">保存</a-button>
                    <a-button size="small" @click="editingCommentId = null">取消</a-button>
                  </div>
                </div>
                <div v-else>{{ item.content }}</div>
              </template>
            </a-list-item-meta>
            <template #actions v-if="isCommentAuthor(item) && editingCommentId !== item.id">
              <a-button type="link" size="small" @click="startEditComment(item)">编辑</a-button>
              <a-popconfirm title="确定删除这条评论？" @confirm="handleDeleteComment(item)" ok-text="确定" cancel-text="取消">
                <a-button type="link" size="small" danger>删除</a-button>
              </a-popconfirm>
            </template>
          </a-list-item>
        </template>
      </a-list>

      <a-divider />

      <div v-if="userStore.isLoggedIn">
        <h4>发表评论</h4>
        <a-textarea v-model:value="commentContent" :rows="3" placeholder="写下你的评论..." />
        <a-button type="primary" style="margin-top: 8px;" @click="handleComment" :loading="commenting">
          发表评论
        </a-button>
      </div>
      <a-alert v-else message="请先登录后再评论" type="warning" show-icon />
      </template>
    </a-card>

    <a-modal v-model:open="showEditModal" title="编辑帖子" :footer="null" width="600px">
      <a-space direction="vertical" style="width: 100%;" :size="12">
        <a-input v-model:value="editForm.title" placeholder="帖子标题" />
        <a-textarea v-model:value="editForm.content" :rows="8" placeholder="帖子内容" />
        <div style="display: flex; gap: 8px; justify-content: flex-end;">
          <a-button v-if="post?.is_draft" @click="handleSaveDraft">保存草稿</a-button>
          <a-button type="primary" @click="handleEdit">保存发布</a-button>
        </div>
      </a-space>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '../store/user'
import { getPostDetail, createComment, updateComment, deleteComment, likePost, favoritePost, updatePost, deletePost } from '../api/posts'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const post = ref<any>(null)
const commentContent = ref('')
const commenting = ref(false)
const showEditModal = ref(false)
const editForm = ref({ title: '', content: '', is_draft: false })
const editingCommentId = ref<number | null>(null)
const editCommentContent = ref('')

const isAuthor = computed(() => {
  if (!post.value || !userStore.isLoggedIn) return false
  return post.value.author === Number(userStore.userId) || post.value.author_name === userStore.username
})

const isFromMy = computed(() => route.query.from === 'my')

const isCommentAuthor = (comment: any) => {
  if (!userStore.isLoggedIn) return false
  return comment.author === Number(userStore.userId) || comment.author_name === userStore.username
}

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

const fetchPost = async () => {
  try {
    const id = Number(route.params.id)
    const res = await getPostDetail(id)
    post.value = res.data
    editForm.value = { title: res.data.title, content: res.data.content, is_draft: res.data.is_draft }
  } catch {
    message.error('获取帖子详情失败')
  }
}

const handleLike = async () => {
  if (!userStore.isLoggedIn) { message.warning('请先登录'); return }
  try {
    const res = await likePost(Number(route.params.id))
    if (post.value) {
      post.value.is_liked = res.data.liked
      post.value.like_count = res.data.like_count
    }
  } catch { message.error('操作失败') }
}

const handleFavorite = async () => {
  if (!userStore.isLoggedIn) { message.warning('请先登录'); return }
  try {
    const res = await favoritePost(Number(route.params.id))
    if (post.value) {
      post.value.is_favorited = res.data.favorited
      post.value.favorite_count = res.data.favorite_count
    }
  } catch { message.error('操作失败') }
}

const handleComment = async () => {
  if (!commentContent.value.trim()) { message.warning('请输入评论内容'); return }
  commenting.value = true
  try {
    await createComment(Number(route.params.id), { content: commentContent.value })
    message.success('评论成功')
    commentContent.value = ''
    fetchPost()
  } catch { message.error('评论失败') }
  finally { commenting.value = false }
}

const startEditComment = (comment: any) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const handleUpdateComment = async (comment: any) => {
  if (!editCommentContent.value.trim()) { message.warning('请输入评论内容'); return }
  try {
    await updateComment(Number(route.params.id), comment.id, { content: editCommentContent.value })
    message.success('评论已更新')
    editingCommentId.value = null
    fetchPost()
  } catch { message.error('更新失败') }
}

const handleDeleteComment = async (comment: any) => {
  try {
    await deleteComment(Number(route.params.id), comment.id)
    message.success('评论已删除')
    fetchPost()
  } catch { message.error('删除失败') }
}

const handleEdit = async () => {
  if (!editForm.value.title) { message.warning('请填写标题'); return }
  try {
    await updatePost(Number(route.params.id), { ...editForm.value, is_draft: false })
    message.success('帖子已更新')
    showEditModal.value = false
    fetchPost()
  } catch { message.error('更新失败') }
}

const handleSaveDraft = async () => {
  if (!editForm.value.title) { message.warning('请填写标题'); return }
  try {
    await updatePost(Number(route.params.id), { ...editForm.value, is_draft: true })
    message.success('草稿已保存')
    showEditModal.value = false
    router.push('/my/drafts')
  } catch { message.error('保存失败') }
}

const handleDelete = async () => {
  try {
    await deletePost(Number(route.params.id))
    message.success('帖子已删除')
    router.push('/')
  } catch { message.error('删除失败') }
}

const handleShare = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    message.success('链接已复制到剪贴板')
  }).catch(() => {
    message.info(`分享链接: ${url}`)
  })
}

onMounted(() => {
  fetchPost()
  userStore.restoreFromStorage()
})
</script>
