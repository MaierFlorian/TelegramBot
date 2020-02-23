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

    @bot.message_handler(commands=["spam"])
    def spam_msg(m):
        cid = m.chat.id
        args = m.text.split()
        num = 10
        msg = "spam"
        if len(args) >= 2:
            try:
                num = int(args[1])
            except ValueError:
                num = 0
        if len(args) == 3:
            msg = args[2]
        if num == 0:
            num = 1
            msg = "Usage: `/spam [num [msg]]`"
        for _ in range(num):
            bot.send_message(cid, msg, parse_mode="Markdown")

    @bot.message_handler(commands=["reminder"])
    def reminder(m):
        cid = m.chat.id
        args = m.text.split()

        if len(args) != 3:
            bot.reply_to(m, f"Usage: `/{args[0]} <HH:MM:SS> <what>`")
            return
        

    @bot.message_handler(commands=["help"])
    def help(m):
        bot.reply_to(m, "Available **commands** are:\n* hh\n* start\n* spam\n") #TODO find out why parse mode does not work

    @bot.message_handler(content_types=['new_chat_members'])
    def greetings(m):
        new_member = ', '.join([x.first_name for x in m.new_chat_members])
        bot.send_message(m.chat.id, f"hello {new_member}");
        knownUsers.append([x.first_name for x in m.new_chat_members])

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
