from rest_framework import viewsets, filters, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

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
    """Вьюсет для подписчиков."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )

    def get_queryset(self):
        return self.request.user.user.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
