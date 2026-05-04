import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/auth-process',
    name: 'AuthProcess',
    component: () => import('../views/AuthProcessView.vue'),
  },
  {
    path: '/post-process',
    name: 'PostProcess',
    component: () => import('../views/PostProcessView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/auth-security',
    name: 'AuthSecurity',
    component: () => import('../views/AuthSecurityView.vue'),
  },
  {
    path: '/attack-process',
    name: 'AttackProcess',
    component: () => import('../views/AttackProcessView.vue'),
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetailView.vue'),
  },
  {
    path: '/my/:type',
    name: 'MyContent',
    component: () => import('../views/MyContentView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  const userId = localStorage.getItem('user_id')
  const isLoggedIn = !!(token || userId)

  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
