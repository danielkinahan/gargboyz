from django.urls import path
from .views import meme_list, meme_add, meme_edit, meme_add_multiple

urlpatterns = [
    path('', meme_list, name='meme_list'),
    path('add/', meme_add, name='meme_add'),
    path('add/multiple/', meme_add_multiple, name='meme_add_multiple'),
    path('edit/<int:pk>/', meme_edit, name='meme_edit'),
]
