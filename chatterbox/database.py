from collections import namedtuple
import sqlite3


class Word:
    def __init__(self, id, value, count):
        self.id = id
        self.value = value
        self.count = count


class Database:
    start_sentence_id = 0
    end_sentence_id = 1
    chain_length = 5

    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.initialise_tables()

    def initialise_tables(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY,
                word TEXT,
                count INTEGER
            );

            INSERT OR IGNORE INTO dictionary VALUES (0, '', 1);
            INSERT OR IGNORE INTO dictionary VALUES (1, '', 1);

            CREATE TABLE IF NOT EXISTS chains (
                id INTEGER PRIMARY KEY,
                word1 INTEGER,
                word2 INTEGER,
                word3 INTEGER,
                word4 INTEGER,
                word5 INTEGER
            );
        """

        self.cursor.executescript(sql)
        self.commit()

    @property
    def cursor(self):
        try:
            return self._cursor
        except AttributeError:
            self._cursor = self.db.cursor()
            return self._cursor

    def close_cursor(self):
        self._cursor.close()
        del self._cursor

    def commit(self):
        self.db.commit()
        self.close_cursor()

    @property
    def words(self):
        try:
            return self._words
        except AttributeError:
            self._words = {}
            self.cursor.execute('SELECT id, word, count FROM dictionary')
            for row in self.cursor:
                self._words[row[1]] = Word(row[1], row[0], row[2])
            return self._words

    def add_word(self, word):
        if word not in self.words:
            sql = 'INSERT INTO dictionary (word, count) VALUES (?, 1)'
            self.cursor.execute(sql, (word,))
            self.words[word] = Word(self.cursor.lastrowid, word, 1)
        else:
            sql = 'UPDATE dictionary SET count = count + 1 WHERE word = ?'
            self.cursor.execute(sql, (word,))
            self.words[word].count += 1

    def add_words(self, words):
        for word in words:
            self.add_word(word)

        if words:
            self.commit()

    def _convert_chain(self, chain):
        converted = []
        for entry in chain:
            if isinstance(entry, int):
                converted.append(entry)
            elif isinstance(entry, str):
                converted.append(self.words[entry].id)
            else:
                raise TypeError(entry)
        return converted

    def add_chain(self, chain):
        chain = self._convert_chain(chain)
        sql = """
            INSERT INTO chains (word1, word2, word3, word4, word5)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, chain)

    def add_chains(self, chains):
        for chain in chains:
            self.add_chain(chain)

        if chains:
            self.commit()
