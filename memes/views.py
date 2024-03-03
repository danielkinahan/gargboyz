from django.shortcuts import render, redirect
from .forms import MemeAddForm, MemeEditForm, MemeAddFormSet
from .models import Meme


def meme_list(request):
    memes = Meme.objects.all()
    return render(request, 'meme_list.html', {'memes': memes})


def meme_add(request):
    if request.method == 'POST':
        form = MemeAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the list view after successful submission
            return redirect('meme_list')
    else:
        form = MemeAddForm()
    return render(request, 'meme_form.html', {'form': form})


def meme_add_multiple(request):
    if request.method == 'POST':
        formset = MemeAddFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                # Perform any additional processing on each instance if needed
                instance.save()
            # Redirect to the appropriate URL after saving
            return redirect('meme_list')
    else:
        formset = MemeAddFormSet()
    return render(request, 'meme_form_multiple.html', {'formset': formset})


def meme_edit(request, pk):
    meme = Meme.objects.get(pk=pk)
    if request.method == 'POST':
        form = MemeEditForm(request.POST, instance=meme)
        if form.is_valid():
            form.save()
            return redirect('meme_list')
    else:
        form = MemeEditForm(instance=meme)
    return render(request, 'meme_form.html', {'form': form})
