# This example requires the 'message_content' intent.

import base64
import discord
from PIL import Image
from io import BytesIO
from logic import FusionBrainAPI
from config import APIKEY, SECRETKEY, TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$generate'):
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', APIKEY, SECRETKEY)
        pipeline_id = api.get_pipeline()
        uuid = api.generate(message.content.replace("$generate", "", 1), pipeline_id)
        files = api.check_generation(uuid)

        # Dekode string Base64 menjadi data biner    
        decoded_data = base64.b64decode(files[0])

        # Buat objek gambar menggunakan PIL
        image = Image.open(BytesIO(decoded_data))

        image.save("decoded_image.png")  # Menyimpan gambar ke dalam memori
        await message.channel.send(file=discord.File("decoded_image.png"))
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)