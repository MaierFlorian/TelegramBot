import telebot
import time
import os 
import sys
import argparse
from importlib import import_module

""" DEFAULT CONFIGURATION """
default_configuration = {
        "config_file": "./config",                          # the config file
        "modules": ["reddit", "hhInteract", "reminder"],    # default loaded modules
        "token_file": "token.txt",
        "token": None,
        "verbosity": 0                                      # verbosity level
        }

def init_config():
    configuration = {}
    #parse cli arg TODO
    parser = argparse.ArgumentParser(description="Run a Telegram Bot")
    parser.add_argument("-v", "--verbose", action="count")
    parser.add_argument("-c", "--config_file", metavar="file", help="overrides the default configuration file location")
    parser.add_argument("-t", "--token", metavar="TOKEN", help="provide the token for the Telegram API")
    parser.add_argument("--token_file", metavar="file", help="provide a file containing the Telegram API token, as an alternative to `-t`")
    parser.add_argument("-m", "--modules", metavar="module", nargs="+", help="specify the modules you want to load")
    ns = parser.parse_args(sys.argv[1:])
    
    for k, v in vars(ns).items():
        if v != None:
            configuration[k] = v
    
    if "token" in configuration and "token_file" in configuration:
        print("Only a token or a token file can be specified")
        sys.exit(1)

    #read config file, if present TODO
    #load the defaults for still unset options
    for k, v in default_configuration.items():
        if k not in configuration:
            configuration[k] = v

    return configuration

def main():
    configuration = init_config()

    if configuration["token"] == None:
        with open(configuration["token_file"]) as f:
            token = f.readline().strip()
    else:
        token = configuration["token"]
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
	    bot.reply_to(message, "Moin")    

    @bot.message_handler(commands=["help", "h"])
    def help(m):
        bot.reply_to(m, "Available **commands** are:\n\- start\n\- help\n\- spam\n\- r / reddit / meme\n", parse_mode="Markdownv2")

    #now we can import
    for m in configuration["modules"]:
        mod = import_module(m)
        mod.init(bot)

    bot.polling()

if __name__ == "__main__":
    main()
