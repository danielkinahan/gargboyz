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

    average_rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)


    def update_average_rating(self):
        avg_rating = Rating.objects.filter(meme=self).aggregate(Avg("rating"))["rating__avg"] or 0
        self.average_rating = avg_rating or 0
        self.save()
        return avg_rating

    def update_rating_count(self):
        rating_cnt = Rating.objects.filter(meme=self).count()
        self.rating_count = rating_cnt
        self.save()
        return rating_cnt

    def update_comment_count(self):
        comment_cnt = Comment.objects.filter(meme=self).count()
        self.comment_count = comment_cnt
        self.save()
        return comment_cnt

    def user_rating(self, user):
        try:
            rating = Rating.objects.get(meme=self, user=user)
            return rating.rating
        except Rating.DoesNotExist:
            return 0

    def __str__(self):
        return f"Meme {self.number}"


class Comment(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{} - {}'.format(self.user, self.body)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.meme.number}: {self.rating}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.meme.update_average_rating()