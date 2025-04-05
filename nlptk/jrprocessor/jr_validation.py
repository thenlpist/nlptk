
import json
import logging
import os
from json import JSONDecodeError
from logging import handlers
from pathlib import Path

import jsonschema
from jsonschema.exceptions import ValidationError

# from status_codes import StatusCode

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
    VALIDATION_APPROACH =  "jsonschema"  #"pydantic"

    def __init__(self):
        self.resume_schema = self._load_resume_schema()

    def validate_json(self, obj):
        print(f"validate_json type(obj) {type(obj)}")
        match self.VALIDATION_APPROACH:
            case "jsonschema":
                return self.validate_json_w_jsonschema(obj)
            case _:
                return self.validate_json_w_jsonschema(obj)

    def validate_json_w_jsonschema(self, obj):
        valid_json = False
        valid_json_resume = False
        if isinstance(obj, dict):
            valid_json = True
            valid_json_resume = self._is_valid_json_resume(obj)
        else:
            try:
                d = json.loads(obj)
                valid_json = True
                valid_json_resume = self._is_valid_json_resume(d)
            except (JSONDecodeError, TypeError) as e:
                logger.error(f"JSONValidationError: invalid json for generated object: {obj}")
        return valid_json, valid_json_resume


    def _is_valid_json_resume(self, d):
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

    def compute_statuscode(self, response):
        valid_json = response["is_valid_json"]
        valid_jsonresume = response["is_valid_jsonresume"]

        if valid_json == True and valid_jsonresume == True:
            response["jsonresume"] = self._jsonresume_to_dict(response)
            statuscode = StatusCode.OK

        elif valid_json == True and valid_jsonresume == False:
            statuscode = StatusCode.INVALID_JSON_RESUME

        elif valid_json == False and valid_jsonresume == False:
            statuscode = StatusCode.NONPARSEABLE_JSON

        else:
            statuscode = StatusCode.INTERNAL_SERVER_ERROR

        return response, statuscode

    def _jsonresume_to_dict(self, response):
        if isinstance(response["jsonresume"], dict):
            jsonresume = response["jsonresume"]
        else:
            jsonresume = json.loads(response["jsonresume"])
        return jsonresume
