import telebot
import time
import os 
import sys
from importlib import import_module

""" DEFAULT CONFIGURATION """
default_configuration = {
        "config_file": "./config",                          # the config file
        "modules": ["reddit", "hhInteract", "reminder"],    # default loaded modules
        "verbosity": 0                                      # verbosity level
        }

def init_config():
    configuration = {}
    #parse cli arg TODO
    #check if an config file is set via a cli arg
    #read config file, if present TODO
    #load the defaults for still unset options
    for k, v in default_configuration.items():
        if k not in configuration:
            configuration[k] = v

    return configuration

def main():
    configuration = init_config()

    with open("token.txt") as f:
        token = f.readline().strip()
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
	    bot.reply_to(message, "Moin")    

    @bot.message_handler(commands=["help", "h"])
    def help(m):
        bot.reply_to(m, "Available **commands** are:\n* start\n* help\n* spam\n* r / reddit / meme\n", parse_mode="Markdownv2") #TODO find out why parse mode does not work

    #now we can import
    for m in configuration["modules"]:
        mod = import_module(m)
        mod.init(bot)

    bot.polling()

if __name__ == "__main__":
    main()
