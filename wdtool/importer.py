from .util import mkdir_if_not_exists
from dataknead import Knead
from pathlib import Path
import json
import logging
import requests

logger = logging.getLogger(__name__)
MAX_QIDS_PER_API_CALL = 50
WD_API_ENDPOINT = "https://www.wikidata.org/w/api.php"

class Importer:
    def __init__(self, path, data_path, key = None, has_header = False):
        logger.debug(f"Importing {path} to {data_path}")
        self.data_path = data_path
        self.key = key
        self.path = path
        self.qids = Knead(path, has_header = has_header).map(self._cleanup).data()
        logger.debug(f"Found {len(self.qids)} ids")

    def _cleanup(self, row):
        if self.key:
            val = row[self.key]
        else:
            val = row

        return val.replace("http://www.wikidata.org/entity/", "")

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
