import requests
import mimetypes
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater

# Your bot token from BotFather
TOKEN = '7695421396:AAEqwYSEi2IjVGkoauoLMvXlURE1jIh5XMM'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Send me a link to any file, and I will fetch and send it to you!')

def fetch_file(url: str):
    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return filename
    else:
        return None

def send_file(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text(f'Fetching file from {url}...')
    
    # Fetch the file
    file_path = fetch_file(url)
    
    if file_path:
        # Determine file type using mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # If the file is a video
        if mime_type and mime_type.startswith('video'):
            with open(file_path, 'rb') as video:
                context.bot.send_video(chat_id=update.effective_chat.id, video=video)
        
        # If the file is a PDF
        elif mime_type == 'application/pdf':
            with open(file_path, 'rb') as pdf:
                context.bot.send_document(chat_id=update.effective_chat.id, document=pdf)
        
        # If the file is an image
        elif mime_type and mime_type.startswith('image'):
            with open(file_path, 'rb') as image:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        
        # If the file is any other type
        else:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    
    else:
        update.message.reply_text("Failed to fetch the file. Please check the URL.")

def main():
    # Create an updater object with the bot token
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Handler to fetch and send file
    dispatcher.add_handler(CommandHandler("getfile", send_file))

    # Start polling
    updater.start_polling()

    # Run the bot until the user sends a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
