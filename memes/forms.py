from django import forms
from .models import Meme
from django.forms import ValidationError, formset_factory
import os

from pydub import AudioSegment
import speech_recognition as sr


class MemeEditForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meme_created_at'].required = False
        self.fields['voice_recording_created_at'].required = False

    meme_created_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    voice_recording_created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class MemeAddForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meme_created_at'].required = False
        self.fields['voice_recording_created_at'].required = False
        self.fields['meme_type'].widget = forms.HiddenInput()
        self.fields['voice_recording_transcript'].widget = forms.HiddenInput()

    meme_created_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    voice_recording_created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


MemeAddFormSet = formset_factory(MemeAddForm)
