from django_filters import FilterSet, ModelMultipleChoiceFilter
from django.template.defaulttags import register
from django.forms.widgets import CheckboxSelectMultiple
from .models import Meme, Author


class MemeFilter(FilterSet):

    authors = ModelMultipleChoiceFilter(
        field_name='authors',  # Specify the field name in the Meme model
        queryset=Author.objects.all(),  # Replace Author with your actual model name
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),  # Use CheckboxSelectMultiple widget
        label='Authors',  # Optionally specify a custom label
        conjoined=True,
    )
    class Meta:
        model = Meme
        fields = {
            "voice_recording_transcript": ["icontains"],
            "authors": ["exact"],
            "season": ["exact"],
        }



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_non_zero(dictionary):
    return {key: value for key, value in dictionary.items() if value != 0}

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter
def times_desc(start, end):
    return range(start, end - 1, -1)

@register.filter
def add_half(number):
    return float(number) + 0.5