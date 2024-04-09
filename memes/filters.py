from django_filters import FilterSet
from .models import Meme

class MemeFilter(FilterSet):
    class Meta:
        model = Meme
        fields = {
            "voice_recording_transcript": ["icontains"],
            "authors": ["exact"],
        }

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_non_zero(dictionary):
    return {key: value for key, value in dictionary.items() if value != 0}