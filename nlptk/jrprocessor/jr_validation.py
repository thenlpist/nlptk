import json
import logging
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

# file_logger = bool(os.environ.get("FILE_LOGGER", False))
# if file_logger:
#     # Set up file handler
#     LOGFILE = "LOGS/resume_parser.log"
#     fh = handlers.RotatingFileHandler(LOGFILE, maxBytes=100000, backupCount=10)
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
logger.addHandler(sh)


class JRValidate:
    # app_dir = Path(__file__).parent.resolve()
    # RESUME_SCHEMA_PATH = app_dir.joinpath("jsonresume_schema.json")
    app_dir = Path(__file__).parent.parent.resolve()
    # print(f"app_dir:  {app_dir}")
    RESUME_SCHEMA_PATH = app_dir.joinpath("jrdatamodel", "jsonresume_schema_20250414.json")

    # print(f"RESUME_SCHEMA_PATH:  {RESUME_SCHEMA_PATH}")

    def __init__(self):
        self.resume_schema = self._load_resume_schema()

    def is_valid_json_resume(self, d):
        try:
            jsonschema.validate(instance=d, schema=self.resume_schema)
            return True
        except ValidationError as e:
            logger.error(f"In json path:  {e.json_path}, {e.message}")
            return False

    def _load_resume_schema(self):
        with open(self.RESUME_SCHEMA_PATH) as fo:
            return json.loads(fo.read())


    # Unused placeholder for if I want to compute and validate coverage of extracted text
    # def validate_approx_coverage(self, d, text):
    def validate_approx_coverage(self, d):
        values = self._get_all_values(d)
        extracted_text = " ".join([v for v in values if v])
        len_values = len(extracted_text)
        # coverage = len(extracted_text) / len(text)
        # return false if less than 1% of text is extracted. (e.g. when the resume is actually a cover letter)
        # if coverage < 0.01:
        #     return False
        # return True
        # arbitrarily return false if less than 100 characters are extracted
        if len_values < 100:
            return False
        return True

    def _get_all_values(self, nested_dict):
        values = []
        for value in nested_dict.values():
            if isinstance(value, dict):
                values.extend(self._get_all_values(value))
            elif isinstance(value, list):
                [values.extend(self._get_all_values(v)) for v in value]
            else:
                values.append(value)
        return values
