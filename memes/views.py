from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .forms import MemeAddForm, MemeEditForm, MemeAddFormSet
from .models import Meme
from .utils import get_extension, transcribe_audio
from .serializers import MemeSerializer


def read(request):
    memes = Meme.objects.all()
    return render(request, 'meme_list.html', {'memes': memes})


@api_view(['POST'])
def api_create(request):
    serializer = MemeSerializer(data=request.data)
    if serializer.is_valid():
        meme_path = serializer.validated_data.get('meme_path')
        voice_recording_path = serializer.validated_data.get(
            'voice_recording_path')

        if meme_path:
            serializer.validated_data['meme_type'] = get_extension(
                meme_path)

        if voice_recording_path:
            serializer.validated_data['voice_recording_transcript'] = transcribe_audio(
                voice_recording_path)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create(request):
    form = MemeAddForm(request.POST, request.FILES)
    if form.is_valid():
        meme_path = request.FILES.get('meme_path')
        voice_recording_path = request.FILES.get(
            'voice_recording_path')

        if meme_path:
            form.instance.meme_type = get_extension(meme_path)

        if voice_recording_path:
            form.instance.voice_recording_transcript = transcribe_audio(
                voice_recording_path)

        form.save()
        return redirect('read')

    return render(request, 'meme_form.html', {'form': form})


def create_multiple(request):
    if request.method == 'POST':
        formset = MemeAddFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                # Perform any additional processing on each instance if needed
                instance.save()
            # Redirect to the appropriate URL after saving
            return redirect('read')
    else:
        formset = MemeAddFormSet()
    return render(request, 'meme_form_multiple.html', {'formset': formset})


def update(request, pk):
    meme = Meme.objects.get(pk=pk)
    if request.method == 'POST':
        form = MemeEditForm(request.POST, instance=meme)
        if form.is_valid():
            form.save()
            return redirect('read')
    else:
        form = MemeEditForm(instance=meme)
    return render(request, 'meme_form.html', {'form': form})
