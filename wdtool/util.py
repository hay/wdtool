import logging
import os

logger = logging.getLogger(__name__)

class UserException(Exception):
    pass

def mkdir_if_not_exists(path):
    if not os.path.isdir(path):
        logging.info(f"{path} does not exist, creating")
        os.mkdir(path)