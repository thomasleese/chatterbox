import time
import random

import irc.bot


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, generator, channels, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.generator = generator
        self.channels_to_join = channels
        self.nick = nickname

    def on_nicknameinuse(self, c, e):
        self.nick = c.get_nickname() + '_'
        c.nick(self.nick)

    def on_welcome(self, c, e):
        for channel in self.channels_to_join:
            c.join(channel)

    def on_privmsg(self, c, e):
        sentence = self.generator.generate_sentence()
        time.sleep((random.random() + 1) * 0.015 * len(sentence))
        c.privmsg(e.source.nick, sentence)

    def on_pubmsg(self, c, e):
        if self.nick in e.arguments[0]:
            sentence = self.generator.generate_sentence()
            time.sleep((random.random() + 1) * 0.015 * len(sentence))
            c.privmsg(e.target, sentence)
