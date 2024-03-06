from django.db import models

# Create your models here.

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meme(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True)
    declared_number = models.PositiveBigIntegerField(blank=True, null=True)
    meme_path = models.FileField(upload_to='memes/', blank=True)
    meme_type = models.CharField(max_length=50, blank=True)
    meme_created_at = models.DateField(blank=True)
    voice_recording_path = models.FileField(
        upload_to='recordings/', blank=True)
    voice_recording_created_at = models.DateTimeField(blank=True)
    voice_recording_transcript = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    season = models.PositiveSmallIntegerField(blank=True, null=True)
    subseason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Meme {self.number}"
