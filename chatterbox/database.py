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
