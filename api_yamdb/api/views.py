from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer)

from .models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    lookup_field = 'name'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
