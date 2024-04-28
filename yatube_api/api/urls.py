from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PostsViewSet,
    FollowListCreate,
    CommentsViewSet,
    GroupViewSet
)

router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(
    'posts/(?P<post_id>[^/.]+)/comments',
    CommentsViewSet, basename='post-comments'
)
router.register('follow', FollowListCreate, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(r'v1/', include('djoser.urls.jwt')),
]
