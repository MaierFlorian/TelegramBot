import telebot
import time
import os 

import reddit

def main():
    with open("token.txt") as f:
        token = f.readline().strip()
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
	    bot.reply_to(message, "Moin")    

    @bot.message_handler(commands=["help", "h"])
    def help(m):
        bot.reply_to(m, "Available **commands** are:\n* hh\n* start\n* spam\n") #TODO find out why parse mode does not work

    #now we can import
    reddit.init(bot)

    bot.polling()

if __name__ == "__main__":
    main()
