from django.urls import path

from . import views

urlpatterns = [
    path('title/<int:title_id>/comment/', views.add_comment, name='add_comment'),
]
