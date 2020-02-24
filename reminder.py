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

        def timespan():
            dur_i = int(args[1][:-1])
            dur_c = args[1][-1]

            if dur_c != 's':
                dur_i *= 60
                if dur_c != 'm':
                    dur_i *= 60
                    if dur_c != 'h':
                        dur_i *= 24
                        if dur_c != 'd':
                            raise ValueError #the character is not an accepted value
            return dur_i

        def fixed_time():
            t = (time.strptime(args[1], "%H:%M"))
            tl = time.localtime()
            tt = list(t)
            tt[3] = tl.tm_hour
            tt[4] = tl.tm_min
            tt[5] = tl.tm_sec

            ts = time.struct_time(tt)

            td = time.mktime(t) - time.mktime(ts)
            print(td)
            if td < 0:
                td += 86400 # add a day if time is before now
            return td

        try:
            duration = timespan()
        except ValueError:
            #either wrong parser or wrongly formatted
            try:
                duration = fixed_time()
            except ValueError:
                usage()
                return

        time.sleep(duration)
        bot.reply_to(message, args[2])

