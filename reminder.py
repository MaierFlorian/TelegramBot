import telebot
import time

def init(bot):
    @bot.message_handler(commands=["reminder", "remind"])
    def reminder_reminder(message):
        args = message.text.split();

        def usage():
            bot.send_message(message.chat.id,
                    f"Usage: {args[0]} <when> <what>")
        
        if len(args) < 3:
            usage()
            return

        try:
            dur_i = int(args[1][:-1])
            print(dur_i)
        except ValueError:
            usage()
            return

        dur_c = args[1][-1]

        if dur_c != 's':
            dur_i *= 60
            if dur_c != 'm':
                dur_i *= 60
                if dur_c != 'h':
                    dur_i *= 24
                    if dur_c != 'd':
                        usage()
                        return

        time.sleep(dur_i)
        bot.reply_to(message, args[2])

