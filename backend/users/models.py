from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, default='', verbose_name='个人简介')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'users_user'

    def __str__(self):
        return self.username


class AccessTokenRecord(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_token_records')
    is_blacklisted = models.BooleanField(default=False, verbose_name='是否已拉黑')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'AccessToken记录'
        verbose_name_plural = verbose_name
        db_table = 'users_access_token_record'

    def __str__(self):
        status = '已拉黑' if self.is_blacklisted else '活跃'
        return f'{self.user.username} - {self.jti[:20]}... ({status})'
