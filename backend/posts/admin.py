from django.contrib import admin
from .models import Post, PostLike, PostFavorite, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'views', 'is_draft', 'created_at']
    list_filter = ['is_draft', 'created_at']
    search_fields = ['title', 'content']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']


@admin.register(PostFavorite)
class PostFavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'created_at']
