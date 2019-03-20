#!/usr/bin/env python3
from argparse import ArgumentParser
from wdtool.constants import COMMANDS, DATA_DIRECTORY, LOOKUP_PATH
from wdtool.importer import Importer
from wdtool.reconciler import Reconciler
import logging
logger = logging.getLogger(__name__)

def get_parser():
    parser = ArgumentParser(description = "Tool to match strings to Wikidata items")

    parser.add_argument("command", choices = COMMANDS, nargs = "?")

    parser.add_argument("--has-header", action = "store_true",
        help = "CSV file has a header"
    )

    parser.add_argument("-i", "--input", type = str, required = True,
        help = "Input CSV file"
    )

    parser.add_argument("-k", "--key", type = str,
        help = "If a CSV file has multiple columns, give the key of the column"
    )

    parser.add_argument("-o", "--output", type = str,
        help = "Output CSV file"
    )

    parser.add_argument("-dp", "--data-path", type = str, default = DATA_DIRECTORY,
        help = f"Path where the JSON Wikidata files will be saved, defaults to {DATA_DIRECTORY}"
    )

    parser.add_argument("-v", "--verbose", action = "store_true",
        help = "Display debug information"
    )

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