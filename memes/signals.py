from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment

@receiver([post_save, post_delete], sender=Comment)
def update_post_comment_count(sender, instance, **kwargs):
    if instance.meme:
        instance.meme.update_comment_count()