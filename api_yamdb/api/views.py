from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAuthorPermission, IsAdminOrReadOnly
from .serializers import (GetTokenSerializer, NotAdminSerializer,
                          SignUpSerializer, UsersSerializer,
                          CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleSerializer)

from reviews.models import Category, Genre, Title, User, Review


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorPermission, IsAuthenticatedOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        post = get_object_or_404(Review, pk=review_id)
        return post.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена. Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена. Поля email и username должны быть уникальными. Пример тела запроса:
    {
        "email": "string",
        "username": "string"
    }
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
