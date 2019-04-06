from .constants import FIELDNAMES, FUZZ_RATIO
from .util import UserException
from dataknead import Knead
from fuzzywuzzy import fuzz
import logging
logger = logging.getLogger(__name__)

class Reconciler:
    def __init__(self, input_path, output_path, lookup_path, key = None):
        self.input_path = input_path
        self.item_count = 0
        self.lookup_path = lookup_path
        self.lookup = self._create_lookup()
        self.match_count = 0
        self.output_path = output_path
        self.key = key

    def _create_lookup(self):
        lookup = {}

        for row in Knead(self.lookup_path).data():
            label = row[0]
            qid = row[1]

            if label in lookup:
                lookup[label].append(qid)
            else:
                lookup[label] = [qid]

        return lookup

    def _lookup(self, inp):
        self.item_count += 1

        if self.key and self.key not in inp:
            raise UserException(f"key '{self.key}' does not exist in the data")
        elif self.key:
            inp = inp[self.key]
        else:
            inp = inp[0]

        logging.debug(f"Trying to match '{inp}'")

        row = {
            "hits" : 0,
            "input" : inp,
            "match_method" : None,
            "qid" : None
        }

        row = self._match_with_name(row)

        if not row["qid"]:
            row = self._match_with_fuzzy(row)

        if row["qid"]:
            self.match_count += 1
        else:
            logging.debug(f"No hits for {inp}")

        return row

    def _match_with_fuzzy(self, row):
        name = row["input"]
        scores = []

        for wd_name, qid in self.lookup.items():
            ratio = fuzz.ratio(name, wd_name)

            if ratio > FUZZ_RATIO:
                scores.append({
                    "name" : wd_name,
                    "ratio" : ratio,
                    "qid" : qid
                })

        if len(scores) == 0:
            return row

        scores.sort(key = lambda r:r["ratio"], reverse = True)
        first = scores[0]

        row.update({
            "qid" : ",".join(first["qid"]),
            "hits" : len(first["qid"]),
            "match_method" : "fuzzy",
            "qlabel" : first["name"],
            "qratio" : first["ratio"]
        })

        logging.debug(
            f'Matched {name} to {row["qlabel"]} ({row["qid"]}) by fuzzy'
        )

        return row

    def _match_with_name(self, row):
        name = row["input"]

        if name in self.lookup:
            qid = self.lookup[name]
            row["hits"] = len(qid)

            if len(qid) > 1:
                logging.warning(f"Warning: There are {len(qid)} results for '{name}'")

            row["qid"] = ",".join(qid)
            row["match_method"] = "lookup"
            logging.debug(f'Matched "{name}" to {row["qid"]} by name')

        return row

    def run(self):
        items = Knead(self.input_path, has_header = self.key is not None).map(self._lookup).data()
        Knead(items).write(self.output_path, fieldnames = FIELDNAMES)