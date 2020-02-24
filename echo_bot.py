import telebot
import time
import os 

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

def main():
    with open("token.txt") as f:
        token = f.readline().strip()
    bot = telebot.TeleBot(token)
    loadMembers()

    @bot.message_handler(func=lambda m: True)
    def add_members(message):
        #if(message.chat.first_name not in knownUsers):
        knownUsers.insert(message.chat.first_name)
        saveMembers()

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
	    bot.reply_to(message, "Moin")

    @bot.message_handler(commands=['hh'])
    def send_hh(message):
        bot.reply_to(message, "Starting to hh. All members have to hh within 60 seconds. Else kick.")
        time.sleep(60.0)
        bot.reply_to(message, ":(")

    @bot.message_handler(commands=['info'])
    def send_info(message):
        bot.send_message(message.chat.id, knownUsers)

    @bot.message_handler(func=lambda message: message.text.lower() == "hh")
    def echo_all(message):
        bot.send_message(message.chat.id, "hh, " + str(message.chat.first_name))
        return message.chat.id

    bot.polling()

def saveMembers():
    with open("members.txt", 'w') as f:
        for s in knownUsers:
            f.write(str(s) +"\n")

def loadMembers():
    if(os.stat("members.txt").st_size != 0):
        with open("members.txt", 'r') as f:
            for line in f:
                knownUsers.insert(str(line.strip()))

if __name__ == "__main__":
    main()
