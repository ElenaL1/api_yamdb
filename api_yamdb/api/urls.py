from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls))
]