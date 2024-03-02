from django.db import models

# Create your models here.

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meme(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True)
    declared_number = models.PositiveBigIntegerField(null=True, blank=True)
    media_path = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=50, blank=True)
    media_created_at = models.DateField(null=True, blank=True)
    voice_recording_path = models.CharField(
        max_length=100, null=True, blank=True)
    voice_recording_created_at = models.DateTimeField(null=True, blank=True)
    voice_recording_transcript = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    season = models.PositiveSmallIntegerField(null=True, blank=True)
    subseason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Meme {self.number}"
