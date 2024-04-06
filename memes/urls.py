from django.urls import path
from .views import *

urlpatterns = [
    path('', read, name='read'),
    path('<int:pk>', detail, name='detail'),
    path('random/', read_random, name='read_random'),
    path('season/<int:season>', read_season, name='read_season'),
    path('create/', create, name='create'),
    path('create/multiple/', create_multiple, name='create_multiple'),
    path('update/<int:pk>/', update, name='update'),
    path('update/all/', update_all, name='update_all'),
    path('api/create/', api_create, name='api_create'),
    path('api/read/', api_read, name='api_read'),
    path('rate/<int:pk>/<int:rating>/', rate, name='rate'),
]
