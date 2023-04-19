

from telethon import TelegramClient, events
import telethon.sync
from telethon.tl.types import InputPeerUser
import os
print('Bot started up!')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TOKEN')

client = TelegramClient('Mediabotica', api_id, api_hash).start(bot_token = bot_token)

@client.on(events.NewMessage(pattern = r'\/id'))
async def id(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        inputt = await replied.get_input_sender()

        if isinstance(inputt, InputPeerUser):
            id = inputt.user_id
        #if isinstance(inputt, In
        await event.reply(str(id))
async def progress(current, total):
    percentage = (current/total)*100
    await msg.edit(f'Downloading video... {percentage:2f} complete.')

@client.on(events.NewMessage(pattern = r'\/start'))
async def start(event):
    await event.respond('I\'m still growing up')

@client.on(events.NewMessage(func = lambda e: e.video))
async def Downloader(event):
    video = event.video
    chat_id = event.chat_id
    
    msg = await client.send_message(chat_id, 'Downloading video...')
    await client.download_media(video, progress_callback = progress) 
    msg.edit('Successfully downloaded video!')

@client.on(events.NewMessage(pattern = r'\/info'))
async def info(event):
    if len(event.raw_text.split()) > 1:
        try:
            if isinstance(int(event.raw_text.split()[1]), int):
                sender_id = int(event.raw_text.split()[1])
                sender = await client.get_entity(sender_id)
        except:
            await event.reply('User not found.')
            sender = None
            
    else:
        if event.is_reply:
            replied = await event.get_reply_message()
            sender = replied.sender
        else:
            sender = await event.get_sender()

        if sender is not None:
            if sender.last_name:
                full_name = sender.first_name + ' ' + sender.last_name
            else:
                full_name = sender.first_name
            photo = await client.download_profile_photo(sender)
            if photo:
                chat_id = event.chat_id
                await client.send_file(chat_id, photo, caption = f'Info of {full_name}: \nPremium user = {sender.premium} \nUsername = {sender.username}')
                os.remove(photo)
            else:
                await event.reply(f'Info of {full_name}: \nPremium user = {sender.premium} \nUsername = {sender.username}')


client.start()
client.run_until_disconnected()
