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
        fields = ['number', 'declared_number', 'meme_path', 'meme_type', 'meme_created_at',
                  'voice_recording_path', 'voice_recording_created_at', 'voice_recording_transcript',
                  'authors', 'season', 'subseason']

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

    def clean(self):
        cleaned_data = super().clean()
        meme_path = cleaned_data.get('meme_path')
        voice_recording_path = cleaned_data.get('voice_recording_path')

        # Populate meme_type based on the uploaded file extension
        if meme_path:
            _, file_extension = os.path.splitext(meme_path.name)
            cleaned_data['meme_type'] = file_extension.strip('.')

        # Check that voice_recording_path is an MP3 file
        if voice_recording_path:
            _, file_extension = os.path.splitext(voice_recording_path.name)
            if file_extension.lower() != '.mp3':
                raise ValidationError('Voice recording must be an MP3 file.')

            temp_audio = "temp.wav"
            sound = AudioSegment.from_mp3(voice_recording_path)
            sound.export(temp_audio, format="wav")

            # transcribe audio file

            # use the audio file as the audio source
            r = sr.Recognizer()
            with sr.AudioFile(temp_audio) as source:
                audio = r.record(source)  # read the entire audio file
                cleaned_data['voice_recording_transcript'] = r.recognize_google(
                    audio)
                print(cleaned_data['voice_recording_transcript'])
            os.remove(temp_audio)
        return cleaned_data


MemeAddFormSet = formset_factory(MemeAddForm)
