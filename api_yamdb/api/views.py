from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from reviews.models import Reviews
from .permissions import IsAuthorPermission

from .serializers import CommentSerializer


class ReviewViewSet(viewsets.ModelViewSe):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorPermission, IsAuthenticatedOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        post = get_object_or_404(Reviews, pk=review_id)
        return post.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Reviews, pk=review_id)
        serializer.save(author=self.request.user, review=review)
