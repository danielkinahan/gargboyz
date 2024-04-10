from django.urls import path
from .views import *

urlpatterns = [
    path('', meme_list, name='list'),
    path('<int:pk>', meme_detail, name='detail'),
    path('random/', meme_random, name='random'),
    path('season/<int:season>', meme_season, name='season'),
    path('create/', meme_create, name='create'),
    path('create/multiple/', meme_create_multiple, name='create multiple'),
    path('update/<int:pk>/', meme_edit, name='edit'),
    path('update/all/', meme_edit_all, name='edit all'),
    path('api/read/', meme_api_list, name='api list'),
    path('api/create/', meme_api_create, name='api create'),
    path('api/update/<int:pk>/', meme_api_edit, name='api edit'),
    path('rate/<int:pk>/<int:rating>/', rate, name='rate'),
]
