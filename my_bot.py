import telebot
import time
import praw
from prawcore import NotFound

def main():
    with open("token.txt") as f:
        token = f.readline().strip()
    bot = telebot.TeleBot(token)

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
        if (len(args) < 2 or len(args) > 4):
            bot.send_message(m.chat.id, "Usage: /r <subreddit> [r=random | t=top | add 'c' for top comment] [all | day | hour | month | week | year]")
            return
        sre = str(args[1])
        period = "week"
        if(len(args) == 4):
            if(str(args[3]) == "all"):
                period = "all"
            elif(str(args[3]) == "day"):
                period = "day"
            elif(str(args[3]) == "hour"):
                period = "hour"
            elif(str(args[3]) == "month"):
                period = "month"
            elif(str(args[3]) == "week"):
                period = "week"
            elif(str(args[3]) == "year"):
                period = "year"
        searchtype = "t"
        if(len(args) >= 3):
            if("r" in str(args[2])):
                searchtype = "r"
            elif("t" in str(args[2])):
                searchtype = "t"
            if("c" in (str(args[2]))):
                searchtype = searchtype + "c"
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


    bot.polling()

def getRedditComment(submission):
    submission.comment_sort = "best"
    submission.comment_limit = 1
    for top_level_comment in submission.comments:
        return top_level_comment.body



if __name__ == "__main__":
    main()