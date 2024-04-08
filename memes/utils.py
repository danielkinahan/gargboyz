import os
from pydub import AudioSegment
import speech_recognition as sr
import ffmpeg
import tempfile

def get_extension(meme_path):
    return os.path.splitext(meme_path.name)[1].strip('.')

def get_media_creation_time(file_path):
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file_path.chunks():
                temp_file.write(chunk)

        # Probe the file to get metadata
        probe = ffmpeg.probe(temp_file.name)
        metadata = next(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')

        # Extract creation time from metadata
        creation_time_str = metadata.get('tags', {}).get('creation_time')

        os.remove(temp_file.name)
        return creation_time_str

    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e} {e.stderr}")
        return None
    except Exception as e:
        print(f"Error extracting media creation time: {e}")
        return None

def transcribe_audio(voice_recording_path):

    sound = AudioSegment.from_file(voice_recording_path)
    temp_audio = "temp.wav"
    sound.export(temp_audio, format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(temp_audio) as source:
        audio = r.record(source)  # Read the entire audio file
    try:
        transcript = r.recognize_google(audio)
        os.remove(temp_audio)
    except:
        os.remove(temp_audio)
        return "Transcription failed"

    return transcript
