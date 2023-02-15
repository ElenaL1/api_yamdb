from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'


class TitleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'title'
