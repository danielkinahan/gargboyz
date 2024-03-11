from django import forms
from .models import Meme
from django.forms import formset_factory


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
        # self.fields['meme_created_at'].required = False
        # self.fields['voice_recording_created_at'].required = False
        self.fields['meme_type'].widget = forms.HiddenInput()
        self.fields['voice_recording_transcript'].widget = forms.HiddenInput()
        self.fields['meme_path'].label = "Meme"
        self.fields['voice_recording_path'].label = "Idea"
        self.fields['meme_path'].help_text = "Meme image or video file"
        self.fields['voice_recording_path'].help_text = "Idea voice recording"

    meme_created_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    voice_recording_created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    field_order = ('number', 'meme_path', 'voice_recording_path',  
        'authors', 'declared_number', 'voice_recording_created_at', 'season', 'meme_created_at', 'subseason')



MemeAddFormSet = formset_factory(MemeAddForm)
