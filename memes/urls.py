from django.urls import path
from .views import read, create, update, create_multiple, api_create, api_read

urlpatterns = [
    path('', read, name='read'),
    path('create/', create, name='create'),
    path('create/multiple/', create_multiple, name='create_multiple'),
    path('update/<int:pk>/', update, name='update'),
    path('api/create/', api_create, name='api_create'),
    path('api/read/', api_read, name='api_read'),
]
