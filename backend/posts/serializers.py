from rest_framework import serializers
from .models import Post, PostLike, PostFavorite, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['post', 'author', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author_name', 'like_count', 'favorite_count',
                  'comment_count', 'views', 'is_liked', 'is_favorited',
                  'is_draft', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return obj.likers.filter(id=user.id).exists()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return obj.favoriters.filter(id=user.id).exists()


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_name',
                  'like_count', 'favorite_count', 'comment_count', 'views',
                  'is_liked', 'is_favorited', 'is_draft',
                  'comments', 'created_at', 'updated_at']
        read_only_fields = ['author', 'views', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return obj.likers.filter(id=user.id).exists()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return obj.favoriters.filter(id=user.id).exists()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'is_draft']
        read_only_fields = ['id']
