from dataknead import Knead
from .util import mkdir_if_not_exists
import logging
logger = logging.getLogger(__name__)

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

    def _import(self):
        to_scrape = []

        for qid in self.qids:
            print(qid)

    def run(self):
        mkdir_if_not_exists(self.data_path)
        self._import()
