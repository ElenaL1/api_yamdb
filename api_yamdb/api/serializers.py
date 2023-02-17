from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(
        regex=r'^[-a-zA-Z0-9_]+$',
        max_length=50,
        required=True
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(
        regex=r'^[-a-zA-Z0-9_]+$',
        max_length=50,
        required=True
    )

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='name', many=True, read_only=True)
    category = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = ('id', 'name', 'genre', 'category')
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'post')
        model = Comment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role'
        )
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )
