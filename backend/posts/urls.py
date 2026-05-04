from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PostViewSet, basename='post')
router.register(r'(?P<post_pk>[^/.]+)/comments', views.CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
]
