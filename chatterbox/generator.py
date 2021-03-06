class Generator:
    chain_length = 3  # different to database chain length

    def __init__(self, database):
        self.database = database

    def generate_sentence(self):
        words = []

        chain = self.database.find_chain([self.database.start_sentence_id])

        while True:
            # take first word
            for word in chain[:1]:
                words.append(self.database.words[word].value)

            # use the next four words to find the next chain
            next_chain = self.database.find_chain(chain[1:self.chain_length])
            if next_chain is None:
                for word in chain[1:]:
                    words.append(self.database.words[word].value)
                break

            chain = next_chain

        return ' '.join(words).strip()

    def generate_text(self, length=40):
        sentences = []
        for i in range(length):
            sentences.append(self.generate_sentence())
        return ' '.join(sentences)
