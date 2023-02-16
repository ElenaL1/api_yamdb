from django.urls import path, include
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, TitleViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
