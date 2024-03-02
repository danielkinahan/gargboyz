from django import forms
from .models import Meme


class MemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = '__all__'
