from django.db import models
from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    is_draft = models.BooleanField(default=False, verbose_name='是否草稿')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    likers = models.ManyToManyField(User, through='PostLike', related_name='liked_posts', verbose_name='点赞用户')
    favoriters = models.ManyToManyField(User, through='PostFavorite', related_name='favorite_posts', verbose_name='收藏用户')

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        db_table = 'posts_post'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likers.count()

    @property
    def favorite_count(self):
        return self.favoriters.count()

    @property
    def comment_count(self):
        return self.comments.count()


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes', verbose_name='用户')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes', verbose_name='帖子')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '帖子点赞'
        verbose_name_plural = verbose_name
        db_table = 'posts_postlike'
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'


class PostFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_favorites', verbose_name='用户')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_favorites', verbose_name='帖子')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '帖子收藏'
        verbose_name_plural = verbose_name
        db_table = 'posts_postfavorite'
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} favorited {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='所属帖子')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'posts_comment'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'
