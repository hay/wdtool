from dataknead import Knead
from fuzzywuzzy import fuzz
import logging
logger = logging.getLogger(__name__)

FUZZ_RATIO = 80

class Reconciler:
    def __init__(self, input_path, output_path, lookup_path):
        self.input_path = input_path
        self.item_count = 0
        self.lookup_path = lookup_path
        self.lookup = { r[0]:r[1] for r in Knead(self.lookup_path).data() }
        self.match_count = 0
        self.output_path = output_path

    def _lookup(self, inp):
        self.item_count += 1
        inp = inp[0]
        logging.debug(f"Trying to match '{inp}'")

        row = {
            "input" : inp,
            "match_method" : None,
            "qid" : None
        }

        row = self._match_with_name(row)

        if not row["qid"]:
            row = self._match_with_fuzzy(row)

        if row["qid"]:
            self.match_count += 1

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

        row["qid"] = first["qid"]
        row["match_method"] = "fuzzy"
        row["qlabel"] = first["name"]
        row["qratio"] = first["ratio"]

        logging.debug(
            f'Matched {name} to {row["qlabel"]} ({row["qid"]}) by fuzzy'
        )

        return row

    def _match_with_name(self, row):
        name = row["input"]

        if name in self.lookup:
            row["qid"] = self.lookup[name]
            row["match_method"] = "lookup"
            logging.debug(f'Matched "{name}" to {row["qid"]} by name')

        return row

    def run(self):
        items = Knead(self.input_path).map(self._lookup).data()
        Knead(items).write(self.output_path)