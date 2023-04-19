from telethon.sync import events, TelegramClient
import os
from telethon.tl.types import DocumentAttributeFilename
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TOKEN')

client = TelegramClient('Mediabotica', api_id, api_hash).start(bot_token = bot_token)


@client.on(events.NewMessage(func = lambda e: e.video))
async def video_download(event):
    video = event.video
    filename_attr = next((attr for attr in video.attributes if isinstance(attr, DocumentAttributeFilename)), None)
    file_name = filename_attr.file_name if filename_attr else 'Video.mp4'
    chat_id = event.chat_id
    async def progress(current, total):
        downloaded = current/1024
        full_size = total/1024
        progress = f'{downloaded/1024:.2f}/{full_size/1024:.2f}'
        await client.edit_message(msg, f'Downloading video... {progress}')
    msg = await client.send_message(chat_id, 'Downloading video...')
    await client.download_media(video, file_name, progress_callback = progress)
    await client.edit_message(chat_id, msg, 'Download complete.')

client.start()
client.run_until_disconnected()
