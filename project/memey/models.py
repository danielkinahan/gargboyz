from django.db import models

# Create your models here.
from django.db import models


class Meme(models.Model):
    media_path = models.FilePathField(max_length=200)
    media_type = models.CharField(max_length=200)
    media_created_at = models.DateTimeField("date meme'd")
    voice_recording_path = models.FilePathField(max_length=200)
    voice_recording_created_at = models.DateTimeField("date recorded")
    voice_recording_transcript = models.TextField()
    authors = models.CharField(max_length=200)  # Change this later
    season = models.PositiveSmallIntegerField()
    subseason = models.CharField(max_length=200)
