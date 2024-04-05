from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meme(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True)
    declared_number = models.PositiveBigIntegerField(blank=True, null=True)
    meme_path = models.FileField(upload_to='memes/', blank=True)
    meme_thumbnail = ImageSpecField(source='meme_path',
                                    processors=[ResizeToFit(100, 100)],
                                    format='JPEG',
                                    options={'quality': 90})
    meme_type = models.CharField(max_length=50, blank=True)
    meme_created_at = models.DateField(blank=True)
    voice_recording_path = models.FileField(
        upload_to='recordings/', blank=True)
    voice_recording_created_at = models.DateTimeField(blank=True)
    voice_recording_transcript = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    season = models.PositiveSmallIntegerField(blank=True, null=True)
    subseason = models.CharField(max_length=100, blank=True)


    def average_rating(self) -> float:
        return Rating.objects.filter(meme=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    # def user_rating(self, user):
    #     try:
    #         rating = Rating.objects.get(meme=self, user=user)
    #         return rating.rating
    #     except Rating.DoesNotExist:
    #         return 0

    def __str__(self):
        return f"Meme {self.number}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.meme.number}: {self.rating}"