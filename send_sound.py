import requests
import io


with open('sound.wav', 'rb') as f:
    data = f.read()

    response = requests.post(
        'http://127.0.0.1:5000/recognize',
        json={
            'audio': repr(data)
        },
    )
    print(response.text)
