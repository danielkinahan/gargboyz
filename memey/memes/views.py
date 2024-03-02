from django.shortcuts import render, redirect
from .forms import MemeForm
from .models import Meme


def meme_list(request):
    memes = Meme.objects.all()
    return render(request, 'memes/meme_list.html', {'memes': memes})


def meme_add(request):
    if request.method == 'POST':
        form = MemeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meme_list')
    else:
        form = MemeForm()
    return render(request, 'memes/meme_form.html', {'form': form})


def meme_edit(request, pk):
    meme = Meme.objects.get(pk=pk)
    if request.method == 'POST':
        form = MemeForm(request.POST, instance=meme)
        if form.is_valid():
            form.save()
            return redirect('meme_list')
    else:
        form = MemeForm(instance=meme)
    return render(request, 'memes/meme_form.html', {'form': form})
