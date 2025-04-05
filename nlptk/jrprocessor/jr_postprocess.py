import copy
import logging
import os
import re
from logging import handlers

import json_repair

from nlptk.jrprocessor.jr_validation import JRValidate

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


class JRPostProcess:

    def postprocess(self, parser_response: str):
        response = self._clean_response(copy.copy(parser_response))
        d = json_repair.loads(response)
        is_valid_json = False
        is_valid_jsonresume = False
        if not d:
            return parser_response, is_valid_json, is_valid_jsonresume

        d = self._none_to_empty_str(d)  # convert NONE values to ""
        d = self._strip_value(d)  # remove any leading/training whitespace from values
        is_valid_json = True

        validate = JRValidate()
        is_valid_jsonresume = validate.is_valid_json_resume(d)
        return d, is_valid_json

    def _clean_response(self, text):
        text = re.sub("<unk>", " ", text)  # strip the <unk> tokens from the response
        text = re.sub("##", "", text)  # strip markdown header tags added by document parser
        text = re.sub(" ?u2022", "", text)  # remove incomplete unicode bullet characters
        text = re.sub(" +", " ", text)  # normalize any duplicate spaces left by above
        return text

    def _none_to_empty_str(self, obj):
        if obj != None:
            if isinstance(obj, dict):
                return {k: self._none_to_empty_str(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [self._none_to_empty_str(x) for x in obj]
            return obj
        logger.debug(f"Converting obj {obj} to string...")
        return ""

    def _strip_value(self, obj):
        if isinstance(obj, dict):
            return {k: self._strip_value(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._strip_value(x) for x in obj]
        return obj.strip()
