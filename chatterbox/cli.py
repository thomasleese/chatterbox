from argparse import ArgumentParser

from .database import Database
from .importer import Importer
from .generator import Generator


def import_command(args):
    database = Database(args.database)
    importer = Importer(database)
    importer.import_directory(args.path)


def speak_command(args):
    database = Database(args.database)
    generator = Generator(database)
    print(generator.generate_sentence())


def main():
    parser = ArgumentParser()
    parser.add_argument('--database', default='chatterbox.sqlite3')

    subparsers = parser.add_subparsers()

    parser_import = subparsers.add_parser('import')
    parser_import.add_argument('path')
    parser_import.set_defaults(func=import_command)

    parser_speak = subparsers.add_parser('speak')
    parser_speak.set_defaults(func=speak_command)

    args = parser.parse_args()

    args.func(args)
