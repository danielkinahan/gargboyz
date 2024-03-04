from django.urls import path
from .views import read, create, update, create_multiple, api_create

urlpatterns = [
    path('', read, name='read'),
    path('create/', create, name='create'),
    path('create/multiple/', create_multiple, name='create_multiple'),
    path('update/<int:pk>/', update, name='update'),
    path('api/create/', api_create, name='api_create'),
]
