from django import forms
from .models import Meme, Comment
from django.forms import formset_factory


class MemeEditForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = '__all__'
        exclude = ['average_rating', 'rating_count', 'comment_count']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voice_recording_created_at'].required = False
        self.fields['meme_created_at'].required = False

    meme_created_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    voice_recording_created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class MemeCreateForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = '__all__'
        exclude = ['average_rating', 'rating_count', 'comment_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meme_created_at'].required = False
        self.fields['meme_type'].widget = forms.HiddenInput()
        self.fields['voice_recording_transcript'].widget = forms.HiddenInput()
        self.fields['voice_recording_created_at'].widget = forms.HiddenInput()
        self.fields['meme_path'].label = "Meme"
        self.fields['voice_recording_path'].label = "Idea"
        self.fields['meme_path'].help_text = "Image, gif or video"
        self.fields['voice_recording_path'].help_text = "Voice recording"

    meme_created_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    
    field_order = ('number', 'meme_path', 'voice_recording_path',  
        'authors', 'declared_number', 'season', 'meme_created_at', 'subseason')

MemeCreateFormSet = formset_factory(MemeCreateForm)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'style':'width: 100%; margin-left: 1rem; margin-bottom: 0;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ""

  