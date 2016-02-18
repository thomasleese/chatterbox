from pathlib import Path

import nltk


class Importer:
    def __init__(self, database):
        self.database = database

        while True:
            try:
                self.tokeniser = nltk.data.load(
                    'tokenizers/punkt/english.pickle')
            except LookupError:
                nltk.download()
            else:
                break

    def find_sentences(self, text):
        return self.tokeniser.tokenize(text)

    def find_words(self, sentence):
        return [word.strip() for word in sentence.split() if word.strip()]

    def find_chains(self, words):
        words.insert(0, self.database.start_sentence_id)
        words.append(self.database.end_sentence_id)

        for i in range(len(words) - self.database.chain_length + 1):
            yield words[i:i + self.database.chain_length]

    def import_text(self, filename):
        print('Importing:', filename)
        with open(filename) as file:
            sentences = self.find_sentences(file.read())
            for sentence in sentences:
                words = self.find_words(sentence)
                self.database.add_words(words)

                chains = list(self.find_chains(words))
                self.database.add_chains(chains)

    def import_directory(self, name):
        path = Path(name)
        for filename in path.iterdir():
            self.import_text(str(filename))
