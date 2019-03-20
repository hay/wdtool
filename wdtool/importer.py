from .constants import ALLOWED_LANGUAGES, MAX_QIDS_PER_API_CALL, WD_API_ENDPOINT
from .util import mkdir_if_not_exists
from dataknead import Knead
from glob import glob
from pathlib import Path
import json
import logging
import requests

logger = logging.getLogger(__name__)

class Importer:
    def __init__(
        self, path, data_path, lookup_path,
        key = None, has_header = False
    ):
        logger.debug(f"Importing {path} to {data_path}")
        self.data_path = data_path
        self.key = key
        self.label_count = 0
        self.lookup_path = lookup_path
        self.path = path
        self.qid_count = 0
        self.qids = Knead(path, has_header = has_header).map(self._cleanup).data()
        logger.debug(f"Found {len(self.qids)} ids")

    def _cleanup(self, row):
        if self.key:
            val = row[self.key]
        else:
            val = row

        return val.replace("http://www.wikidata.org/entity/", "")

    def _create_lookup_table(self):
        lookup = []
        json_path = str(Path(f"{self.data_path}/*.json"))
        logging.debug(f"Getting all data files from {json_path}")

        for path in glob(json_path):
            logging.debug(f"Parsing {path}")
            item = Knead(path).data()
            qid = item["id"]
            labels = self._get_all_labels(item)
            self.qid_count += 1

            for label in labels:
                lookup.append([label, qid])

        self.label_count = len(lookup)
        logging.debug(f"Found {self.label_count} labels")
        logging.debug(f"Writing lookup table to {self.lookup_path}")
        Knead(lookup).write(self.lookup_path)

    def _get_all_labels(self, item):
        labels = set()

        for lang, val in item["labels"].items():
            if lang in ALLOWED_LANGUAGES:
                labels.add(val["value"])

        for lang, vals in item["aliases"].items():
            if lang in ALLOWED_LANGUAGES:
                for val in vals:
                    labels.add(val["value"])

        return list(sorted(labels))

    def _get_qid_data_path(self, qid):
        return Path(f"{self.data_path}/{qid}.json")

    def _import(self):
        to_scrape = []

        for qid in self.qids:
            logger.debug(f"Handling {qid}")
            path = self._get_qid_data_path(qid)

            if Path(path).exists():
                logger.debug(f"{path} exists, skipping")
                continue

            to_scrape.append(qid)

            if len(to_scrape) == MAX_QIDS_PER_API_CALL:
                self._scrape_qids(to_scrape)
                to_scrape = []

        # We probably have some things to scrape left in the array, let's do that
        if len(to_scrape) > 0:
            self._scrape_qids(to_scrape)
        else:
            logger.debug("Nothing to scrape!")

    def _scrape_qids(self, qids):
        req = requests.get(WD_API_ENDPOINT, params = {
            "action" : "wbgetentities",
            "format" : "json",
            "ids" : "|".join(qids)
        })

        logging.debug(f"Doing API call with {len(qids)} qids")

        if req.status_code != 200:
            raise Exception(f"Request error: {req.status_code}")

        for qid, data in req.json()["entities"].items():
            path = self._get_qid_data_path(qid)

            with open(path, "w") as f:
                json_data = json.dumps(data)
                f.write(json_data)
                logging.debug(f"Saved {path}")

    def run(self):
        mkdir_if_not_exists(self.data_path)
        self._import()
        self._create_lookup_table()
