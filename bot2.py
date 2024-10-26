from telebot import TeleBot

TOKEN = "7572549807:AAFCrBBoxS9Jn3DKpK-_YdLEZKyaUCqwKCQ"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Hello, I'm your bot!")

bot.infinity_polling()
