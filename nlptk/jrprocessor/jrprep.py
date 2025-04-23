import logging
import os
import re
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
# if file_logger:
#     # Set up file handler
#     LOGFILE = "LOGS/resume_parser.log"
#     fh = handlers.RotatingFileHandler(LOGFILE, maxBytes=100000, backupCount=10)
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
logger.addHandler(sh)


class PreProcess:

    def __init__(self):
        self.bullet_pat = initial_bullet_pattern()
        self.single_quote_pat = re.compile("[\u02BB\u02BC\u066C\u2018\u2019-\u201A\u275B\u275C]", re.UNICODE)
        self.double_quote_pat = re.compile("[‟\u201C-\u201E\u2033\u275D\u275E\u301D\u301E]", re.UNICODE)
        self.apostrophe_pat = re.compile(
            "[‛\u0027\u02B9\u02BB\u02BC\u02BE\u02C8\u02EE\u0301\u0313\u0315\u055A\u05F3\u07F4\u07F5\u1FBF\u2018\u2019\u2032\uA78C\uFF07]",
            re.UNICODE)

    def process(self, text):
        text = self._clean_input(text)
        return text

    def _clean_input(self, text):
        text = self.bullet_pat.sub("-", text)
        text = self.single_quote_pat.sub("'", text)
        text = self.double_quote_pat.sub('"', text)
        text = self.apostrophe_pat.sub("'", text)
        return text
