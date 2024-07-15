import os
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

updater = Updater(token=TOKEN, use_context=True)


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Hi, I\'m xHamster video bot :)')


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Dude, what are you doing here :/')


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()

updater.idle()
