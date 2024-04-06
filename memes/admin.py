from django.contrib import admin
from .models import Meme, Author, Rating, Comment

# Register your models here.

admin.site.register(Meme)
admin.site.register(Author)
admin.site.register(Rating)
admin.site.register(Comment)
