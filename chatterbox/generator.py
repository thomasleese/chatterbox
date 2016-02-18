class Generator:
    def __init__(self, database):
        self.database = database

    def generate_sentence(self, max_length=50):
        words = []

        chain = self.database.find_chain([self.database.start_sentence_id])

        while len(words) < max_length:
            # take first three words
            for word in chain[:3]:
                words.append(self.database.words[word].value)

            # use the next two words to find the next chain
            next_chain = self.database.find_chain(chain[3:])
            if next_chain is None:
                for word in chain[3:]:
                    words.append(self.database.words[word].value)
                break

            chain = next_chain

        return ' '.join(words).strip()

    def generate_text(self, length=40):
        sentences = []
        for i in range(length):
            sentences.append(self.generate_sentence())
        return ' '.join(sentences)
