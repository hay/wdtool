from pathlib import Path

ALLOWED_LANGUAGES = ("en", "nl", "de", "fr", "es", "it") # This should be user-defined
COMMANDS = ("import", "reconcile")
DATA_DIRECTORY = str(Path(__file__).parent.parent.joinpath("data"))
FIELDNAMES = ("qid", "input", "match_method", "qlabel", "qratio")
FUZZ_RATIO = 80
LOOKUP_PATH = str(Path(f"{DATA_DIRECTORY}/qid-lookup.csv"))
MAX_QIDS_PER_API_CALL = 50
WD_API_ENDPOINT = "https://www.wikidata.org/w/api.php"