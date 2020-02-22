import telebot
import time

bot = telebot.TeleBot("939974039:AAExAMFIvn5zkSEx60I_bx4iXyYGbeLZn7g")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "hihi, bl, lol")

@bot.message_handler(commands=['hh'])
def send_hh(message):
    bot.reply_to(message, "Starting to hh. All members have to hh within 60 seconds. Else kick.")
    time.sleep(60.0)
    bot.reply_to(message, ":(")

bot.polling()