from django.urls import path
from .views import meme_list

urlpatterns = [
    path('', meme_list, name='meme_list'),
]
