from django.urls import path
from .views import *

urlpatterns = [
    path('', read, name='read'),
    path('random/', read_random, name='read_random'),
    path('create/', create, name='create'),
    path('create/multiple/', create_multiple, name='create_multiple'),
    path('update/<int:pk>/', update, name='update'),
    path('api/create/', api_create, name='api_create'),
    path('api/read/', api_read, name='api_read'),
]
