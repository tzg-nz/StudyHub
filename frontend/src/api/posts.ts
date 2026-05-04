import http from '../utils/request'

export function getPostList(params?: { page?: number; search?: string }) {
  return http.get('/posts/', { params })
}

export function getPostDetail(id: number) {
  return http.get(`/posts/${id}/`)
}

export function createPost(data: { title: string; content: string; is_draft?: boolean }) {
  return http.post('/posts/', data)
}

export function updatePost(id: number, data: { title: string; content: string; is_draft?: boolean }) {
  return http.put(`/posts/${id}/`, data)
}

export function deletePost(id: number) {
  return http.delete(`/posts/${id}/`)
}

export function likePost(id: number) {
  return http.post(`/posts/${id}/like/`)
}

export function favoritePost(id: number) {
  return http.post(`/posts/${id}/favorite/`)
}

export function getMyPosts(params?: { page?: number; search?: string }) {
  return http.get('/posts/my_posts/', { params })
}

export function getMyFavorites(params?: { page?: number }) {
  return http.get('/posts/my_favorites/', { params })
}

export function getMyDrafts(params?: { page?: number }) {
  return http.get('/posts/my_drafts/', { params })
}

export function getComments(postId: number) {
  return http.get(`/posts/${postId}/comments/`)
}

export function createComment(postId: number, data: { content: string }) {
  return http.post(`/posts/${postId}/comments/`, data)
}

export function updateComment(postId: number, commentId: number, data: { content: string }) {
  return http.put(`/posts/${postId}/comments/${commentId}/`, data)
}

export function deleteComment(postId: number, commentId: number) {
  return http.delete(`/posts/${postId}/comments/${commentId}/`)
}
