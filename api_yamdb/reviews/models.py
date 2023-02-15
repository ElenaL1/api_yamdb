from django.contrib.auth.models import AbstractUser

from django.db import models

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