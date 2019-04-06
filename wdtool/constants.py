from pathlib import Path

ALLOWED_LANGUAGES = ("en", "nl", "de", "fr", "es", "it") # This should be user-defined
COMMANDS = ("import", "reconcile")
FIELDNAMES = ("qid", "input", "match_method", "hits", "qlabel", "qratio")
FUZZ_RATIO = 80
MAX_QIDS_PER_API_CALL = 50
WD_API_ENDPOINT = "https://www.wikidata.org/w/api.php"