import telebot
import time

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

def main():
    with open("token.txt") as f:
        token = f.readline().strip()
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def command_start(m):
        cid = m.chat.id
        if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
            knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
            userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
            bot.send_message(cid, "Hello, stranger, let me scan you...")
            bot.send_message(cid, "Scanning complete, I know you now")
        else:
            bot.send_message(cid, "I already know you, no need for me to scan you again!")

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

if __name__ == "__main__":
    main()
