import telebot
import time
import praw
from prawcore import NotFound
import re

def init(bot):
    #with open("token.txt") as f:
    #    token = f.readline().strip()
    #bot = telebot.TeleBot(token)

    print("reading reddit")

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
	    bot.reply_to(message, "Moin")

    @bot.message_handler(commands=['help'])
    def send_help(message):
	    bot.reply_to(message, "Available commands:\n\\r or \\reddit or \\meme")

    @bot.message_handler(func=lambda message: message.text.lower() == "hh")
    def echo_all(message):
        bot.send_message(message.chat.id, "hh, " + str(message.chat.first_name))
        return message.chat.id
    
    @bot.message_handler(commands=['r', 'reddit', 'meme'])
    def send_meme(m):
        args = m.text.split()

        def usage():
            bot.send_message(m.chat.id, f"Usage: /{args[0]} <subreddit> [r=random | t=top | add 'c' for top comment] [all | day | hour | month | week | year]")

        if (len(args) < 2 or len(args) > 4):
            usage()
            return
        sre = str(args[1])
        period = "week"
        if(len(args) == 4):
            if(str(args[3]) == "all" or str(args[3]) == "a"):
                period = "all"
            elif(str(args[3]) == "day" or str(args[3]) == "d"):
                period = "day"
            elif(str(args[3]) == "hour" or str(args[3]) == "h"):
                period = "hour"
            elif(str(args[3]) == "month" or str(args[3]) == "m"):
                period = "month"
            elif(str(args[3]) == "week" or str(args[3]) == "w"):
                period = "week"
            elif(str(args[3]) == "year" or str(args[3]) == "y"):
                period = "year"
            else:
                bot.send_message(m.chat.id, "Third parameter sounds wrong. Keep going with \"week\"")
        searchtype = "t"
        if(len(args) >= 3):
            searchtype = ""
            c, r, t = False, False, False
            for arg in args[2]:
                if arg == "c" and not c:
                    c = True
                    searchtype = searchtype + "c"
                elif arg == "r" and not r and not t:
                    r = True
                    searchtype = searchtype + "r"
                elif arg == "t" and not t and not r:
                    t = True
                    searchtype = searchtype + "t"
                else:
                    usage()
                    return
        if("r" not in searchtype and "t" not in searchtype):
            usage()
            return
        reddit = praw.Reddit(client_id = '7xGfOpN5x80H0w', 
                     client_secret = '6eS8fb2mTW8Q5EcqGqcNvE_pxRY', 
                     user_agent = 'meme-collector')
        sr = reddit.subreddit(sre)
        found = False
        try:
            reddit.subreddits.search_by_name(sre, exact=True)
            found = True
        except NotFound:
            bot.send_message(m.chat.id, "Subreddit not found :(")
        if found:
            try:
                if("r" in searchtype):
                    subr = sr.random()
                    bot.send_photo(m.chat.id, subr.url, caption=subr.title)
                    if("c" in searchtype):
                        bot.send_message(m.chat.id, getRedditComment(subr))
                elif ("t" in searchtype):
                    subr = list(sr.top(period))[0]
                    bot.send_photo(m.chat.id, (subr.url), caption=subr.title)
                    if("c" in searchtype):
                        bot.send_message(m.chat.id, getRedditComment(subr))
            except:
                bot.send_message(m.chat.id, "Something is wrong with this subreddit.")
    


    #bot.polling()

def getRedditComment(submission):
    submission.comment_sort = "best"
    submission.comment_limit = 1
    for top_level_comment in submission.comments:
        return top_level_comment.body
