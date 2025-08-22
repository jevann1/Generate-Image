import json
import time
import requests
import base64
from PIL import Image
from io import BytesIO
from config import KEY, SECRET

class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        print(data)
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', KEY, SECRET)
    pipeline_id = api.get_pipeline()
    uuid = api.generate("Butterfly in the sky", pipeline_id)
    files = api.check_generation(uuid)

    # Dekode string Base64 menjadi data biner    
    decoded_data = base64.b64decode(files[0])

    # Buat objek gambar menggunakan PIL
    image = Image.open(BytesIO(decoded_data))

    # Menampilkan gambar (opsional)
    image.show()
    image.save("decoded_image.png")  # Menyimpan gambar ke dalam memori