import json
import logging
import os
from logging import handlers
from pathlib import Path

import jsonschema
from jsonschema.exceptions import ValidationError

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


class JRValidate:
    app_dir = Path(__file__).parent.resolve()
    RESUME_SCHEMA_PATH = app_dir.joinpath("jsonresume_schema.json")

    def __init__(self):
        self.resume_schema = self._load_resume_schema()

    def is_valid_json_resume(self, d):
        try:
            jsonschema.validate(instance=d, schema=self.resume_schema)
            return True
        except ValidationError as e:
            logger.error \
                (f"JSONResumeValidationError: json schema does not conform to jsonresume. Error message: {e.message}")
            logger.error(e.schema)
            return False

    def _load_resume_schema(self):
        with open(self.RESUME_SCHEMA_PATH) as fo:
            return json.loads(fo.read())
