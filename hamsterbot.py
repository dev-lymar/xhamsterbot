import os
import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL')

TOKEN = os.getenv('TOKEN')

updater = Updater(token=TOKEN, use_context=True)


def get_new_video():
    try:
        response = requests.get(URL).json()
    except Exception as error:
        print(error)
        new_url = os.getenv('ERROR_URL')
        response = requests.get(new_url).json()

    random_url = response[0].get('url')
    return random_url


def new_video(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_video())


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Send me video ;)']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Dude, what are you doing here... '
        f'\nI know everything about you, {update.message.chat.first_name}!',
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_video())
    context.bot.send_message(chat_id=chat.id, text='Yeah,  it\'s kitties, and you wanted something else?')


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, new_video))

updater.start_polling()

updater.idle()
