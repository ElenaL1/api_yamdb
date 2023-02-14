from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Класс категорий."""

    name = models.CharField('категория', max_length=100,)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс жанров."""

    name = models.CharField('жанр', max_length=100,)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField('произведение', max_length=100,)
    year = models.IntegerField('год выпуска')
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL, 
        verbose_name='жанр',
        related_name='title')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        related_name='title'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведение'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'соответствие жанра и произведения'
        verbose_name_plural = 'таблица соответствия жанров и произведений'

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'
