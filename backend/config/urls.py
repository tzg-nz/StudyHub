"""
URL配置 - StudyHub项目路由入口
包含三种认证方式的API路由：
- /api/auth/session/*  -> Session认证相关接口
- /api/auth/token/*    -> Token(JWT)认证相关接口
- /api/auth/cookie/*   -> Cookie认证相关接口
- /api/posts/*         -> 帖子相关接口（需要认证）
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
]
