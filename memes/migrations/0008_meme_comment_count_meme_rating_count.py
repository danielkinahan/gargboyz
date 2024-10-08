# Generated by Django 5.0.3 on 2024-04-06 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memes', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='comment_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='meme',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
