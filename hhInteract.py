import telebot
import time

def init(bot):

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

    @bot.message_handler(content_types=['new_chat_members'])
    def greetings(m):
        new_member = ', '.join([x.first_name for x in m.new_chat_members])
        bot.send_message(m.chat.id, f"hello {new_member}")


    membershh = []
    @bot.message_handler(func=lambda message: message.text.lower() == "hh")
    def echo_all(message):
        members = 1
        try:
            members = int(bot.get_chat_members_count(message.chat.id)) - 1
        except:
            print("Counting group members didn't work")
        sender = message.from_user.id
        if(sender not in membershh):
            membershh.append(sender)
        if(len(membershh) == members):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(1)
            bot.send_message(message.chat.id, "hh")
            membershh.clear()