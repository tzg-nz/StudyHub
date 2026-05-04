from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Post, PostLike, PostFavorite, Comment
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            return None


AUTH_CLASSES = [CsrfExemptSessionAuthentication, JWTAuthentication, CookieJWTAuthentication]


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTH_CLASSES
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(is_draft=False)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': '只能修改自己的帖子'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': '只能删除自己的帖子'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_draft:
            Post.objects.filter(pk=instance.pk).update(views=instance.views + 1)
            instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like_obj, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            like_obj.delete()
            return Response({'liked': False, 'like_count': post.like_count})
        return Response({'liked': True, 'like_count': post.like_count})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        post = self.get_object()
        fav_obj, created = PostFavorite.objects.get_or_create(user=request.user, post=post)
        if not created:
            fav_obj.delete()
            return Response({'favorited': False, 'favorite_count': post.favorite_count})
        return Response({'favorited': True, 'favorite_count': post.favorite_count})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        search = request.query_params.get('search')
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_favorites(self, request):
        posts = Post.objects.filter(favoriters=request.user, is_draft=False)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_drafts(self, request):
        posts = Post.objects.filter(author=request.user, is_draft=True)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTH_CLASSES
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs.get('post_pk'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': '只能修改自己的评论'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': '只能删除自己的评论'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
