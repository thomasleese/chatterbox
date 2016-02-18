from argparse import ArgumentParser

from .database import Database
from .importer import Importer


def import_command(args):
    database = Database(args.database)
    importer = Importer(database)
    importer.import_text(args.filename)


def main():
    parser = ArgumentParser()
    parser.add_argument('--database', default='chatterbox.sqlite3')

    subparsers = parser.add_subparsers()

    parser_import = subparsers.add_parser('import')
    parser_import.add_argument('filename')
    parser_import.set_defaults(func=import_command)

    args = parser.parse_args()

    args.func(args)
