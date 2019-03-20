#!/usr/bin/env python3
from argparse import ArgumentParser
import logging
logger = logging.getLogger(__name__)

COMMANDS = ("import", "reconcile")

def get_parser():
    parser = ArgumentParser(description = "Tool for Wikidata data usage")
    parser.add_argument("command", choices = COMMANDS, nargs = "?")
    parser.add_argument("-i", "--input", type = str, required = True)
    parser.add_argument("-o", "--output", type = str)
    parser.add_argument("-v", "--verbose", action = "store_true")
    return parser

def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)