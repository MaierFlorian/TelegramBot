import sys
import random

def init(bot, config=None):

    print("loading insult")

    general_insults = []
    targeted_insults = []

    try:
        with open("res/insults.txt") as f:
            for l in f:
                general_insults.append(l)
        with open("res/insults_target.txt") as f:
            for l in f:
                targeted_insulsts.append(l)
    except FileNotFoundError:
        print("[insult] one of the ressources files was not found. Command may not work properly.", file=sys.stderr)

    random.seed(bot)

    def get_general_insult():
        return random.choice(general_insults);

    def get_targeted_insult(user):
        print("[insult] targeted insults are not yet implemented.", file=sys.stderr)
        raise NotImplementedError
        pass        

    
    """ TODO read insults file """
    @bot.message_handler(commands=['insult'])
    def insult_insult(m):
        args = m.text.split()
        def usage():
            bot.send_message(m.chat.id, f"Usage: {args[0]} [user]")

        if len(args) == 1:
            bot.send_message(m.chat.id, get_general_insult())
        elif len(args) == 2:
            #TODO check if really a user
            bot.send_message(m.chat.id, get_targeted_insult(args[1]))
        else:
            usage()

"""
@return tuple of title and description
"""
def help():
    return ("insult", f"Send an insult into the group. Optionally a user can be specified for a targeted insult\n")

