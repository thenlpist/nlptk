import logging
import os
from logging import handlers

from nlptk.jrprocessor.regex_patterns import initial_bullet_pattern

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create file handler that logs debug and higher level messages
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
sh.setFormatter(formatter)

file_logger = bool(os.environ.get("FILE_LOGGER", False))
if file_logger:
    # Set up file handler
    LOGFILE = "LOGS/resume_parser.log"
    fh = handlers.RotatingFileHandler(LOGFILE, maxBytes=100000, backupCount=10)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
logger.addHandler(sh)


class PreProcess:

    def __init__(self):
        self.bullet_pat = initial_bullet_pattern()

    def process(self, text):
        return self._clean_input(text)

    def _clean_input(self, text):
        self.bullet_pat.sub("-", text)
        return text
