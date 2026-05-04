"""
用户URL配置 - 三种认证方式的API路由

路由结构：
- /api/auth/csrf/             获取CSRF Token
- /api/auth/register/           注册（同时初始化三种认证）
- /api/auth/session/login/      Session登录
- /api/auth/session/logout/     Session登出
- /api/auth/session/profile/    Session获取用户信息
- /api/auth/token/login/        Token登录
- /api/auth/token/refresh/      Token刷新
- /api/auth/token/profile/      Token获取用户信息
- /api/auth/cookie/login/       Cookie登录
- /api/auth/cookie/logout/      Cookie登出
- /api/auth/cookie/profile/     Cookie获取用户信息
- /api/auth/compare/            三种认证方式对比
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('csrf/', views.GetCSRFToken.as_view(), name='csrf-token'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('compare/', views.AuthCompareView.as_view(), name='auth-compare'),
    path('session/login/', views.SessionLoginView.as_view(), name='session-login'),
    path('session/logout/', views.SessionLogoutView.as_view(), name='session-logout'),
    path('session/profile/', views.SessionProfileView.as_view(), name='session-profile'),
    path('token/login/', views.TokenLoginView.as_view(), name='token-login'),
    path('token/logout/', views.TokenLogoutView.as_view(), name='token-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/profile/', views.TokenProfileView.as_view(), name='token-profile'),
    path('cookie/login/', views.CookieLoginView.as_view(), name='cookie-login'),
    path('cookie/logout/', views.CookieLogoutView.as_view(), name='cookie-logout'),
    path('cookie/profile/', views.CookieProfileView.as_view(), name='cookie-profile'),
]
