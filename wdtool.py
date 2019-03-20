#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from wdtool.importer import Importer
from wdtool.reconciler import Reconciler
import logging
logger = logging.getLogger(__name__)

COMMANDS = ("import", "reconcile")
DATA_DIRECTORY = str(Path(__file__).parent.joinpath("data"))
LOOKUP_PATH = str(Path(f"{DATA_DIRECTORY}/qid-lookup.csv"))

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
            has_header = args.has_header,
            lookup_path = LOOKUP_PATH
        )

        importer.run()

        print(f"Found {importer.qid_count} items with {importer.label_count} labels")
    elif args.command == "reconcile":
        reconciler = Reconciler(
            args.input, args.output, lookup_path = LOOKUP_PATH
        )

        reconciler.run()

        matches = reconciler.match_count
        items = reconciler.item_count
        perc = round((matches / items) * 100, 2)
        print(f"{matches} matches found for {items} items ({perc}%)")
    else:
        raise Exception("No command given")

    logging.debug(args)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)