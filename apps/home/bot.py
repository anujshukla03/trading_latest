import telebot

from core.settings import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
print(bot)
@bot.message_handler(commands=["help","hello"])
def send_help_message(msg):
    bot.reply_to(msg,"Hello! This is a test bot")

# to restrict it to text
@bot.message_handler(content_types=["photo","sticker"])
def send_content_message(msg):
    bot.reply_to(msg,"this is not a text message")
#
@bot.message_handler(content_types=["photo","sticker"])
@bot.message_handler(func=lambda msg: msg.from_user.usrname)
def send_content_message(msg):
    bot.reply_to(msg,"this is not a text message")

bot.polling()