from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title


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
