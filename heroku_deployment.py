import os

from dotenv import load_dotenv

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pymongo import MongoClient

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

import googleapiclient.discovery

# sys.path.insert(len(sys.path), '.\\handlers')

# from handler.chloe_ting import chloe_ting_handler
# from handler.generate import generate_handler
# from handler.song_workout import song_workout_handler
# from handler.add_video import add_video_handler 

from handlers import chloe_ting_handler, add_video_handler, generate_handler, song_workout_handler

load_dotenv()

TOKEN = os.getenv('TELE_TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.getLogger(__name__)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# Authenticate with Firebase and create Firestore instance
# cred = credentials.Certificate('./service_account_key.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# Authenticate with MongoDB
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.workout_bot

# Set up Youtube API
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv('GOOGLE_DEVELOPER_KEY')
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY, cache_discovery=False)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    print(update.message.chat)
    update.message.reply_html(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True) # make sure use_context is set to True

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # chloe_ting_text
    # CommandHandler for commands, MessageHandler for messages
    dp.add_handler(CommandHandler("start", start)) 
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("chloeting", chloe_ting_handler))
    dp.add_handler(CommandHandler("generate", lambda update, context: generate_handler(update, context, db)))
    dp.add_handler(CommandHandler("songworkouts", lambda update, context: song_workout_handler(update, context, db)))
    dp.add_handler(CommandHandler("addvideo", lambda update, context: add_video_handler(update, context, youtube, db)))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot by setting the webhook
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook("https://guarded-sea-53454.herokuapp.com/" + TOKEN)

    # Start the bot using polling - kind of like a localhost, the script must be running for the bot to work
    # updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()