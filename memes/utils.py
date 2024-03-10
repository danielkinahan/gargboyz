import os
from pydub import AudioSegment
import speech_recognition as sr


def get_extension(meme_path):
    return os.path.splitext(meme_path.name)[1].strip('.')


def transcribe_audio(voice_recording_path):

    audio_extension = get_extension(voice_recording_path)

    if audio_extension.lower() != 'mp3':
        return "Incorrect extension"

    else:
        temp_audio = "temp.wav"
        sound = AudioSegment.from_mp3(voice_recording_path)
        sound.export(temp_audio, format="wav")
        r = sr.Recognizer()
        with sr.AudioFile(temp_audio) as source:
            audio = r.record(source)  # Read the entire audio file
        try:
            transcript = r.recognize_google(audio)
        except:
            return "Transcription failed"
        os.remove(temp_audio)

        return transcript
