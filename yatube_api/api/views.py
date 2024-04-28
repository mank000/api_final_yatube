from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from posts.models import (
    Post,
    Follow,
    Group
)

from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)

from .permissions import OwnerOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для комментов."""

    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, )

    @staticmethod
    def get_post(post_id):
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_post(self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post(self.kwargs.get('post_id'))
        )


class FollowListCreate(viewsets.ModelViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        search_param = self.request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(
                following__username__icontains=search_param
            )
        return queryset

    def perform_create(self, serializer):
        following_username = self.request.data.get('following')
        if self.request.user.username == following_username:
            raise ValidationError('Невозможно подписаться на себя!')

        following_user = get_object_or_404(User, username=following_username)
        serializer.save(user=self.request.user, following=following_user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
