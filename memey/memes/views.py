from django.shortcuts import render, redirect
from .models import Meme
from .forms import MemeForm


def meme_list(request):
    memes = Meme.objects.all()
    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('meme_list')
    else:
        form = MemeForm()
    return render(request, 'memes/meme_list.html', {'memes': memes, 'form': form})
