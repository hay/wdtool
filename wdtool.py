#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from wdtool.importer import Importer
from wdtool.reconciler import Reconciler
import logging
logger = logging.getLogger(__name__)

COMMANDS = ("import", "reconcile")
DATA_DIRECTORY = Path(__file__).parent.joinpath("data")

def get_parser():
    parser = ArgumentParser(description = "Tool for Wikidata data usage")
    parser.add_argument("command", choices = COMMANDS, nargs = "?")
    parser.add_argument("--has-header", action = "store_true")
    parser.add_argument("-i", "--input", type = str, required = True)
    parser.add_argument("-k", "--key", type = str)
    parser.add_argument("-o", "--output", type = str)
    parser.add_argument("-dp", "--data-path", type = str, default = DATA_DIRECTORY)
    parser.add_argument("-v", "--verbose", action = "store_true")
    return parser

def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.command == "import":
        importer = Importer(
            args.input,
            args.data_path,
            key = args.key,
            has_header = args.has_header
        )
        importer.run()
    elif args.command == "reconcile":
        reconciler = Reconciler(args.input, args.output)
    else:
        raise Exception("No command given")

    logging.debug(args)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)