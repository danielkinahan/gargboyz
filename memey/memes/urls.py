from django.urls import path
from .views import meme_list, meme_add, meme_edit

urlpatterns = [
    path('', meme_list, name='meme_list'),
    path('add/', meme_add, name='meme_add'),
    path('edit/<int:pk>/', meme_edit, name='meme_edit'),
]
