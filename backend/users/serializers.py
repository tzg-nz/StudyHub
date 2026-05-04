"""
用户序列化器 - 用于将用户数据转换为JSON格式
"""
from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, help_text='密码，至少6位')
    password_confirm = serializers.CharField(write_only=True, help_text='确认密码')
    email = serializers.EmailField(required=False, allow_blank=True, default='')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'bio']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text='用户名')
    password = serializers.CharField(help_text='密码')
