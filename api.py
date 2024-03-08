import requests

meme_dir = "/mnt/c/Users/Daniel/Nextcloud/Coding/Archive/Gargboyz PHP Forum/Website.20200819/memeDir/"
rec_dir = "/mnt/c/Users/Daniel/Nextcloud/Coding/Archive/Gargboyz PHP Forum/Website.20200819/memeRecDir/"

username = 'daniel'
password = 'digitalampsneverkill'


def test_create():
    # Example usage
    url = 'http://127.0.0.1:8000/memes/api/create/'
    form_data = {
        'number': '5',
    }

    files = {
        'meme_path': open('uploads/memes/005meme.jpeg', 'rb'),
        'voice_recording_path': open('uploads/recordings/005memeRec.mp3', 'rb'),
    }

    response = requests.post(
        url, data=form_data, files=files, auth=(username, password))

    print("Response Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response)
    print(response.json())


def test_read():
    # Example usage
    url = 'http://127.0.0.1:8000/memes/api/read/'
    response = requests.get(url, auth=(username, password))

    print("Response Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.json())


def post_all_memes():
    # Get the memes from ben on a thumb drive before doing this
    url = 'https://gargboyz.danielkinahan.ca/memes/api/create/'
    count = 161

    for i in range(2, count + 1):
        num_str = str(i).zfill(3)
        form_data = {
            'number': i
        }

        if i != 112:
            files = {
                'meme_path': open(f'{meme_dir}{num_str}meme.jpeg', 'rb'),
                'voice_recording_path': open(f'{rec_dir}{num_str}memeRec.mp3', 'rb'),
            }
        else:
            files = {
                'meme_path': open(f'{meme_dir}{num_str}meme.mp4', 'rb'),
                'voice_recording_path': open(f'{rec_dir}{num_str}memeRec.mp3', 'rb'),
            }
        response = requests.post(
            url, data=form_data, files=files, auth=(username, password))

        print(response)
        print(response.json())


# test_read()
# test_create()
post_all_memes()
