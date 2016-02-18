import time
import random

import irc.bot


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, generator, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.generator = generator
        self.channel = channel
        self.nick = nickname

    def on_nicknameinuse(self, c, e):
        self.nick = c.get_nickname() + '_'
        c.nick(self.nick)

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        sentence = self.generator.generate_sentence()
        time.sleep((random.random() + 1) * 0.02 * len(sentence))
        c.privmsg(e.source.nick, sentence)

    def on_pubmsg(self, c, e):
        if self.nick in e.arguments[0]:
            sentence = self.generator.generate_sentence()
            time.sleep((random.random() + 1) * 0.02 * len(sentence))
            c.privmsg(e.target, sentence)
