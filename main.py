import telebot
import time
import os 
import sys
import argparse
from importlib import import_module

""" DEFAULT CONFIGURATION """
default_configuration = {
        "config_file": "./config",                          # the config file TODO a more decent location for config files
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
        print("Only either a token or a token file can be specified", file=sys.stderr)
        sys.exit(1)

    #read config file, if present TODO
    if "config_file" in configuration:
        #TODO maybe work with ENVVAR for a more global option
        if not os.path.isfile(configuration["config_file"]):
            print("The specified configuration file does not exist", file=sys.stderr)
            sys.exit(2)
    else:
        configuration["config_file"] = default_configuration["config_file"]
    try:
        with open(configuration["config_file"]) as f:
            for l in f.lines():
                if len(l) > 0 and not l.startswith('#'):
                    k, v = map(lambda s: s.strip(), l.split("="))
                    if k == "config_file": #check validity of file contents
                        raise ValueError
                    elif k == "token_file":
                        configuration[k] = v
                        #TODO continue
    except IOError:
        pass
    except ValueError:
        print("The specified configuration file is invalid", file=sys.stderr)
        sys.exit(3)

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
