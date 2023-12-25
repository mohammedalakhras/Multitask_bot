from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InputMediaDocument
import os
import requests




from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload , MediaFileUpload
from google.oauth2.credentials import Credentials

from oauth2client.service_account import ServiceAccountCredentials
import io

#Bard API

#from bardapi import SESSION_HEADERS
#from bardapi import Bard

#token="dwhVsYmoF88n-5syt-g8v6ia1M4T3uTQM7kywk8wC6viRMI04u8KDE4KnIPN9rFnawKTyg."

#session = requests.Session()
#session.headers = SESSION_HEADERS
#session.cookies.set("__Secure-1PSID", token)
#session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBPVxjSrRrsJSyvaVGvoOYsDqyOL2yVlkmaF9Yu3ZA59TOIJjbDLDotdUfCqip1zBZEAA")
#session.cookies.set("__Secure-1PSIDCC", "ABTWhQGNCWpTnhG1HvhUVuIvQpt-NqSNT9snFRVc85WLmqHPTl5UXXfMFp4h_qrlLnKUe20hItY")

#bard = Bard(token=token, session=session)


def gen(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_input = update.message.text
    if not user.username == 'Mohammed_Alakhras':
        caption = f"Gen \nUsername: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)


    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}
    userinput = update.message.text.split(' ', 1)[1]
    if userinput.strip():  # check if input is not empty

        response = requests.post(API_URL, headers=headers, json={"inputs": userinput})
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        image.save('output.png')
        update.message.reply_photo(photo=open('output.png', 'rb'))
        
        os.remove('output.png')
    else:
        update.message.reply_markdown('Please provide a non-empty input.\nsuch as \n/gen tree\n')

    
     
    


def chat(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_input = update.message.text
    if not user.username == 'Mohammed_Alakhras':
        caption = f"Chat \nUsername: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)
    message=' '.join(user_input.split()[1:])
    if message.strip():  # check if input is not empty

       # response = bard.get_answer(message)['content']
        response ="Sorry many Errors,\nUnder Maintenance Now...."
        update.message.reply_text(response)
    else:
        update.message.reply_markdown('Please provide a non-empty input.\nsuch as \n/chat Hello\n')




def up_google_drive_folder(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        folder_id = context.args[0].split('/')[-1]  # extract folder id from url
        credentials = ServiceAccountCredentials.from_json_keyfile_name('bardApp.json', ['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=credentials)

        # Get the list of files in the folder from Google Drive
        results = service.files().list(q=f"'{folder_id}' in parents").execute()
        items = results.get('files', [])

        for file in items:
            file_id = file['id']
            filename = file['name']

            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)

            with open(filename, 'wb') as f:
                f.write(fh.read())
            with open(filename, 'rb') as f:
                context.bot.send_document(chat_id='917477025', document=f, thumb=open('a.png', 'rb'))
            os.remove(filename)
    else:
        update.message.reply_text('عذراً، هذا البوت مخصص فقط للمشرف @Mohammed_Alakhras')
        caption = f"Drive Folder \nUsername: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)

def up_google_drive_file(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        url = context.args[0]
        file_id = url.split('/')[-2]  # extract file id from url
       # file_id = context.args[0].split('/')[-1]  # extract file id from url
        credentials = ServiceAccountCredentials.from_json_keyfile_name('bardApp.json', ['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=credentials)

        # Get the file name from Google Drive
        file = service.files().get(fileId=file_id).execute()
        filename = file['name']

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)

        with open(filename, 'wb') as f:
            f.write(fh.read())
        with open(filename, 'rb') as f:
            context.bot.send_document(chat_id='917477025', document=f, thumb=open('a.png', 'rb'))
        os.remove(filename)
    else:
        update.message.reply_text('عذراً، هذا البوت مخصص فقط للمشرف @Mohammed_Alakhras')
        caption = f"Drive File\n Username: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)



def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        update.message.reply_text('مرحباً @Mohammed_Alakhras')
    else:
        update.message.reply_text('This Bot is intended for its owner only @Mohammed_Alakhras.\nOther users can only use this bot to chat with the PaLM 2 AI model by using chat command:\n/chat YOUR_MESSAGE\nWithin this conversation. ')
        admin_message = f"Start\nUsername: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: [Link](tg://user?id={user.id})"
        context.bot.send_message(chat_id='917477025', text=admin_message, parse_mode='Markdown')

def forward_to_admin(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username != 'Mohammed_Alakhras':
        caption = f"Username: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)



def handle_document(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        attachment = update.message.effective_attachment
        file = context.bot.getFile(attachment.file_id)
        filename = attachment.file_name
        file.download(filename)
        with open(filename, 'rb') as f:
            context.bot.send_document(chat_id='917477025', document=f, thumb=open('a.png', 'rb'))
        os.remove(filename)

    if user.username != 'Mohammed_Alakhras':
        caption = f"Username: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)


def reply_to_user(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras' and update.message.reply_to_message:
        original_sender = update.message.reply_to_message.forward_from.id
        context.bot.send_message(chat_id=original_sender, text=update.message.text)

def handle_video(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        video = update.message.video
        if video is not None:
            file = context.bot.getFile(video.file_id)
            filename = video.file_name
            file.download(filename)
            with open(filename, 'rb') as f:
                context.bot.send_document(chat_id='917477025', document=f, thumb=open('a.png', 'rb'))
            os.remove(filename)

    if user.username != 'Mohammed_Alakhras':
        caption = f"Video \nUsername: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)




def handle_audio(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        audio = update.message.audio
        if audio is not None:
            file = context.bot.getFile(audio.file_id)
            filename = audio.file_name
            file.download(filename)
            with open(filename, 'rb') as f:
                context.bot.send_audio(chat_id='917477025', audio=f, thumb=open('a.png', 'rb'))
            os.remove(filename)

    if user.username != 'Mohammed_Alakhras':
        caption = f"Audio\nUsername: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)

def download_file(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        url = context.args[0]  # Get the URL from the command arguments
        response = requests.get(url, stream=True)

        #if response.headers.get('content-type') == 'application/octet-stream':
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))

        os.remove(filename)
    elif user.username != 'Mohammed_Alakhras':
        update.message.reply_text('عذراً، هذا البوت مخصص فقط للمشرف @Mohammed_Alakhras')
        caption = f"Username: @{user.username}\nID: {user.id}"
        context.bot.forward_message(chat_id='917477025', from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id='917477025', text=caption)
def others(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.username == 'Mohammed_Alakhras':
        update.message.reply_text('مرحباً @Mohammed_Alakhras')
    else:
        update.message.reply_text('عذراً، هذا البوت مخصص فقط للمشرف @Mohammed_Alakhras')
        admin_message = f"Others\nUsername: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: [Link](tg://user?id={user.id})"
        context.bot.send_message(chat_id='917477025', text=admin_message, parse_mode='Markdown')

def AJup_google_drive_folder(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    folder_id = context.args[0].split('/')[-1]  # extract folder id from url
    credentials = ServiceAccountCredentials.from_json_keyfile_name('bardApp.json', ['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)
    # Get the list of files in the folder from Google Drive
    results = service.files().list(q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])

    for file in items:
        file_id = file['id']
        filename = file['name']

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)

        with open(filename, 'wb') as f:
            f.write(fh.read())
        with open(filename, 'rb') as f:
            context.bot.send_document(chat_id=user.id, document=f)
        os.remove(filename)


def main() -> None:
    updater = Updater(os.getenv('token'),use_context=True)

    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("up", up_google_drive_file))
    dispatcher.add_handler(CommandHandler("f", up_google_drive_folder))
    dispatcher.add_handler(CommandHandler("u", download_file))
    dispatcher.add_handler(CommandHandler("n", others))
    dispatcher.add_handler(CommandHandler("b", others))
    dispatcher.add_handler(CommandHandler("c", others))
    dispatcher.add_handler(CommandHandler("a", others))
    dispatcher.add_handler(CommandHandler("v", others))
    dispatcher.add_handler(CommandHandler("pdf", others))
    dispatcher.add_handler(CommandHandler("getnewlectures", others))
    dispatcher.add_handler(CommandHandler("yt", others))

    dispatcher.add_handler(CommandHandler("aj", AJup_google_drive_folder))

    dispatcher.add_handler(CommandHandler("chat", chat))
    dispatcher.add_handler(CommandHandler("gen", gen))


    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, forward_to_admin))
    dispatcher.add_handler(MessageHandler(Filters.document & ~Filters.command, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply & ~Filters.command, reply_to_user))
    #dispatcher.add_handler(MessageHandler(Filters.text , download_file))

    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))
    dispatcher.add_handler(MessageHandler(Filters.audio , handle_audio))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
