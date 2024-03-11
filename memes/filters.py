from django_filters import FilterSet
from .models import Meme

class MemeFilter(FilterSet):
    class Meta:
        model = Meme
        fields = {
            "voice_recording_transcript": ["icontains"],
            "authors": ["exact"],
        }