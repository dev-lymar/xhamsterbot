import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='hamsterbot.log',
    level=logging.INFO,
)

URL = os.getenv('URL')

TOKEN = os.getenv('TOKEN')


def get_new_video():
    """
    Fetches a new URL from the main API.
    If the main API request fails, it fetches the URL from the error API.
    """
    try:
        response = requests.get(URL).json()
    except Exception as error:
        logging.error(f'error during request to the main API: {error}')
        new_url = os.getenv('ERROR_URL')
        response = requests.get(new_url).json()

    random_url = response[0].get('url')
    return random_url


def new_video(update, context):
    """
    Handles the sending of a new video to the user.
    """
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_video())


def wake_up(update, context):
    """
    Greets the user with a message and a random video, and sets up a custom keyboard.
    """
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


def main():
    """
    The basic logic of the bot operation.
    Initializes the bot, sets up the command and message handlers,
    and starts polling for updates.
    """
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, new_video))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
