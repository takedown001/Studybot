import requests
import mimetypes
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application

# Your bot token
TOKEN = 'AAEqwYSEi2IjVGkoauoLMvXlURE1jIh5XMM'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Send me a link to any file, and I will fetch and send it to you!')

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

async def send_file(update: Update, context: CallbackContext):
    url = update.message.text
    await update.message.reply_text(f'Fetching file from {url}...')
    
    # Fetch the file
    file_path = fetch_file(url)
    
    if file_path:
        # Determine file type using mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # If the file is a video
        if mime_type and mime_type.startswith('video'):
            with open(file_path, 'rb') as video:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
        
        # If the file is a PDF
        elif mime_type == 'application/pdf':
            with open(file_path, 'rb') as pdf:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf)
        
        # If the file is an image
        elif mime_type and mime_type.startswith('image'):
            with open(file_path, 'rb') as image:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        
        # If the file is any other type
        else:
            with open(file_path, 'rb') as file:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    
    else:
        await update.message.reply_text("Failed to fetch the file. Please check the URL.")

async def main():
    # Create an application object with the bot token
    application = Application.builder().token(TOKEN).build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Handler to fetch and send file
    application.add_handler(CommandHandler("getfile", send_file))

    # Start polling
    await application.start_polling()

    # Run the bot until the user sends a signal to stop (Ctrl+C)
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
