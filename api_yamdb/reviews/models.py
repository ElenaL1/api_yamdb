from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

from .validators import validate_username, validate_year


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        'ник',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    """Класс категорий."""

    name = models.CharField('категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс жанров."""

    name = models.CharField('жанр', max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50)
        # validators=[RegexValidator(
        #     regex=r'^[-a-zA-Z0-9_]+$',
        #     message='Слаг категории содержит недопустимый символ'
        # )])

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        # constraints = [
        #     UniqueConstraint(
        #         fields=['title', 'genre'],
        #         name='unique_title_genre'),
        #     # CheckConstraint(
        #     #     check=~Q(user=F('following')),
        #     #     name='unique_following')
        # ]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField('произведение', max_length=256,)
    year = models.IntegerField('год выпуска', validators=(validate_year,))
    description = models.CharField('описание', max_length=500,
                                   null=True, blank=True)
    # genre = models.ManyToManyField(
    #     Genre,
    #     verbose_name='жанр',
    #     related_name='title'
    # )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        related_name='title',
        through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        related_name='title',
        null=True
    )
    # rating = models.IntegerField(
    #     verbose_name='Рейтинг',
    #     null=True,
    #     default=None,
    #     blank=True
    # )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведение'
        # constraints = [
        #     UniqueConstraint(
        #         fields=['title', 'genre'],
        #         name='unique_title_genre')
        # ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Только значения от 1 до 10'),
            MaxValueValidator(10, 'Только значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[settings.NUMBER_OF_CHAR]


class Comment(models.Model):
    """Модель комментариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[settings.NUMBER_OF_CHAR]


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
        return f'{self.title} относится к жанру {self.genre}'
