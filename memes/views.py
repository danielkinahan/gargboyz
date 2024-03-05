from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from .forms import MemeAddForm, MemeEditForm, MemeAddFormSet
from .models import Meme
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
    memes = Meme.objects.all()
    return render(request, 'meme_list.html', {'memes': memes})


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

        if voice_recording_path:
            serializer.validated_data['voice_recording_transcript'] = transcribe_audio(
                voice_recording_path)

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
        form = MemeEditForm(request.POST, instance=meme)
        if form.is_valid():
            form.save()
            return redirect('read')
    else:
        form = MemeEditForm(instance=meme)
    return render(request, 'meme_form.html', {'form': form})
