from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import json
import datetime

from .forms import MemeCreateForm, MemeEditForm, MemeCreateFormSet, CommentForm
from .models import Meme, Rating, Comment
from .utils import get_extension, transcribe_audio, get_media_creation_time
from .serializers import MemeSerializer
from .tables import MemeTable
from .filters import MemeFilter


@login_required
def meme_list(request):
    # Get existing query parameters
    memes = Meme.objects.all()

    # Apply filters using django-filters
    filter = MemeFilter(request.GET, queryset=memes)
    has_filter = any(field in request.GET for field in set(filter.get_fields()))
    memes = filter.qs

    sort = request.GET.get('sort')
    if sort:
        memes = memes.order_by(sort)
    else:
        memes = memes.order_by('-number')

    table = MemeTable(memes)

    user_ratings = {meme.pk: meme.user_rating(request.user) for meme in memes}
        
    return render(request, 'memes/list.html', {'table': table, 'filter': filter, 'user_ratings': user_ratings, 'has_filter': has_filter})


@login_required
def meme_detail(request, pk):
    meme = Meme.objects.get(pk=pk)
    comments = Comment.objects.filter(meme__pk=pk)
    ratings = Rating.objects.filter(meme__pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.meme = meme
            new_comment.user = request.user
            new_comment.created_on = datetime.datetime.now()
            new_comment.save()
            comment_form = CommentForm()
            messages.success(request, 'Comment posted')
        else:
            messages.error(request, 'Comment failed')
    else:
        comment_form = CommentForm()

    return render(request, 'memes/detail.html', {'meme': meme, 'ratings': ratings, 'comments': comments, 'comment_form': comment_form})


@login_required
def meme_season(request, season):
    # Get existing query parameters
    memes = Meme.objects.filter(season=season)
    # Apply filters using django-filters
    filter = MemeFilter(request.GET, queryset=memes)
    memes = filter.qs

    sort = request.GET.get('sort')
    if sort:
        memes = memes.order_by(sort)
    else:
        memes = memes.order_by('-number')

    table = MemeTable(memes)

    user_ratings = {meme.pk: meme.user_rating(request.user) for meme in memes}
        
    return render(request, 'memes/list.html', {'table': table, 'filter': filter, 'user_ratings': user_ratings})


@login_required
def meme_random(request):
    memes = Meme.objects.all()

    data = []
    for meme in memes:
        # Append data to list
        meme_meta = {
            'number': meme.number,
            'voice_recording_transcript': meme.voice_recording_transcript,
        }

        try:
            meme_meta['meme_path'] = meme.meme_path.url
        except:
            meme_meta['meme_path'] = ""

        try:
            meme_meta['meme_thumbnail'] = meme.meme_thumbnail.url
        except:
            meme_meta['meme_thumbnail'] = ""

        try:
            meme_meta['voice_recording_path'] = meme.voice_recording_path.url
        except:
            meme_meta['voice_recording_path'] = ""

        data.append(meme_meta)
    return render(request, 'memes/random.html', {'data': json.dumps(data)})

@login_required
def meme_create(request):
    if request.method == 'POST':
        form = MemeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            meme_path = request.FILES.get('meme_path')
            voice_recording_path = request.FILES.get(
                'voice_recording_path')

            if meme_path:
                form.instance.meme_type = get_extension(meme_path)

            if voice_recording_path:
                form.instance.voice_recording_transcript = transcribe_audio(
                    voice_recording_path)
                form.instance.voice_recording_created_at = get_media_creation_time(voice_recording_path)

            form.save()
            messages.success(request, 'New meme successfully created')
            return redirect('list')
        else:
            messages.error(request, 'Meme not saved')
            return render(request, 'memes/form.html', {'form': form})
    else:
        form = MemeCreateForm()
        return render(request, 'memes/form.html', {'form': form})


@login_required
def meme_edit(request, pk):
    meme = Meme.objects.get(pk=pk)
    if request.method == 'POST':
        form = MemeEditForm(request.POST, request.FILES, instance=meme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meme updated')
            return redirect('list')
        else:
            messages.error(request, 'Meme failed to update')
    else:
        form = MemeEditForm(instance=meme)
    return render(request, 'meme/form.html', {'form': form})


@login_required
def meme_create_multiple(request):
    print(request.POST)
    if request.method == 'POST':
        formset = MemeCreateFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            messages.success(request, 'Memes posted')
            return redirect('list')
        else:
            messages.error(request, 'All memes failed to post')
            return render(request, 'memes/create_multiple.html', {'formset': formset})
    else:
        formset = MemeCreateFormSet()
    return render(request, 'meme/create_multiple.html', {'formset': formset})


@login_required
def meme_edit_all(request):
    memes = Meme.objects.all().order_by('-number')
    if request.method == 'POST':
        forms = [MemeEditForm(request.POST, request.FILES, instance=meme_instance,
                              prefix=f'meme-{meme_instance.number}') for meme_instance in memes]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
                # File modifications not working here
            messages.success(request, 'Memes updated')
            return redirect('list')
        else:
            messages.error(request, 'All memes failed to update')
    else:
        forms = [MemeEditForm(
            instance=meme_instance, prefix=f'meme-{meme_instance.number}') for meme_instance in memes]

    packed = zip(forms, memes)
    return render(request, 'memes/edit_all.html', {'packed': packed})


@login_required
def rate(request, pk, rating):

    meme = Meme.objects.get(pk=pk)
    user = request.user
    Rating.objects.filter(meme=meme, user=user).delete()
    Rating.objects.create(user=user, meme=meme, rating=rating)
    meme_rating_count = meme.update_rating_count()
    average_rating = meme.update_average_rating()
    user_rating_count = Rating.objects.filter(user=user).count()

    return JsonResponse({'average_rating': average_rating, 'meme_rating_count': meme_rating_count, 'user_rating_count': user_rating_count})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def meme_api_list(request):
    # Query your model data
    queryset = Meme.objects.all()

    # Serialize the queryset
    serializer = MemeSerializer(queryset, many=True)

    # Return serialized data
    return Response(serializer.data)


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def meme_api_create(request):
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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def meme_api_edit(request, pk):
    try:
        meme = Meme.objects.get(pk=pk)
    except Meme.DoesNotExist:
        return Response({"error": "Meme not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MemeSerializer(meme, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)