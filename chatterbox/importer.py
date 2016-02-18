class Importer:
    def __init__(self, database):
        self.database = database

    def split_line(self, sentence):
        return [word.strip() for word in sentence.split() if word.strip()]

    def import_text(self, filename):
        with open(filename) as file:
            for line in file:
                words = self.split_line(line)
                self.database.add_words(words)
