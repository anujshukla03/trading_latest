from telegram import Bot
from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from django.conf import settings

bot_instance = Bot(settings.TELEGRAM_BOT_TOKEN)
updater = Updater(bot=bot_instance)


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your Django Telegram bot.")


def setup_bot_handlers():
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))


setup_bot_handlers()
updater.start_polling()