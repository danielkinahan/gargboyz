from django.contrib import admin
from .models import Meme, Author, Rating, Comment

@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_filter = ('authors', 'season', 'subseason', 'average_rating', 'rating_count', 'comment_count', 'meme_type')
    search_fields = ('voice_recording_transcript',)

admin.site.register(Author)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'meme', 'rating')
    list_filter = ('user', 'meme', 'rating')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'user', 'meme', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('body',)
