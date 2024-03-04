import requests

# Example usage
form_data = {
    'number': '5',
}

files = {
    'meme_path': open('uploads/memes/005meme.jpeg', 'rb'),
    'voice_recording_path': open('uploads/recordings/005memeRec.mp3', 'rb'),
}

url = 'http://127.0.0.1:8000/memes/api/create/'
response = requests.post(url, data=form_data, files=files)

print(response.json())
