from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import random
import json

from .forms import MemeAddForm, MemeEditForm, MemeAddFormSet
from .models import Meme, Author
from .utils import get_extension, transcribe_audio
from .serializers import MemeSerializer


@api_view(['GET'])
# Use BasicAuthentication for authentication
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_read(request):
    # Query your model data
    queryset = Meme.objects.all()

    # Serialize the queryset
    serializer = MemeSerializer(queryset, many=True)

    # Return serialized data
    return Response(serializer.data)


@login_required
def read(request):
    # Get existing query parameters
    params = QueryDict(request.GET.urlencode(), mutable=True)

    sort_by = params.get('sort_by', 'number')
    direction = params.get('direction', 'desc')
    filter_author = params.get('author', None)

    memes = Meme.objects.all()

    if filter_author:
        memes = memes.filter(authors__name=filter_author)

    if direction == 'asc':
        memes = memes.order_by(sort_by)
    else:
        memes = memes.order_by(f'-{sort_by}')

    page_size = params.get('page_size')

    if page_size == 'all':
        # If 'all' is selected, display all memes without pagination
        memes = memes.all()  # Retrieve all memes without pagination
        page_size = None  # Set page_size to None to indicate all memes
    else:
        # Convert to integer if not 'all'
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        paginator = Paginator(memes, page_size)
        page = params.get('page')

        try:
            memes = paginator.page(page)
        except PageNotAnInteger:
            memes = paginator.page(1)
        except EmptyPage:
            memes = paginator.page(paginator.num_pages)

    authors = Author.objects.all()

    return render(request, 'meme_list.html', {'memes': memes, 'authors': authors, 'page_size': page_size, 'params': params})


@login_required
def read_random(request):
    memes = Meme.objects.all().exclude(meme_path__isnull=True)
    data = []
    for meme in memes:
        # Append data to list
        data.append({
            'number': meme.number,
            'meme_path': meme.meme_path.url,
            'voice_recording_path': meme.voice_recording_path.url,
            'voice_recording_transcript': meme.voice_recording_transcript,
        })
    return render(request, 'meme_random_spin.html', {'data': json.dumps(data)})


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
        try: 
            if voice_recording_path:
                    serializer.validated_data['voice_recording_transcript'] = transcribe_audio(
                        voice_recording_path)
        except:
            serializer.validated_data['voice_recording_transcript'] = " "

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
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


@login_required
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


@login_required
def update(request, pk):
    meme = Meme.objects.get(pk=pk)
    if request.method == 'POST':
        form = MemeEditForm(request.POST, request.FILES, instance=meme)
        if form.is_valid():
            form.save()
            return redirect('read')
    else:
        form = MemeEditForm(instance=meme)
    return render(request, 'meme_form.html', {'form': form})


def update_all(request):
    memes = Meme.objects.all()
    if request.method == 'POST':
        forms = [MemeEditForm(request.POST, request.FILES, instance=meme_instance,
                              prefix=f'meme-{meme_instance.number}') for meme_instance in memes]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
                # File modifications not working here
            return redirect('read')
    else:
        forms = [MemeEditForm(
            instance=meme_instance, prefix=f'meme-{meme_instance.number}') for meme_instance in memes]

    packed = zip(forms, memes)
    return render(request, 'meme_form_all.html', {'packed': packed})
