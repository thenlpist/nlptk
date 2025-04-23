import copy
import logging
import os
import re
from logging import handlers
from typing import Union
import json
import json_repair

from nlptk.jsonresume.converter import Converter
from nlptk.jrprocessor.jr_validation import JRValidate

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


class PostProcess:
    def __init__(self, parser_version=""):
        self.parser_version = parser_version
        self.conv = Converter()

    def postprocess(self, parser_response: Union[str, dict]):
        if isinstance(parser_response, str):
            response = self._clean_response(copy.copy(parser_response))
            d = json_repair.loads(response)
        elif isinstance(parser_response, dict):
            d = parser_response
        else:
            raise ValueError("postprocess argument must be either a str or dict")
        is_valid_json = False
        is_valid_jsonresume = False
        if not d:
            return parser_response, is_valid_json, is_valid_jsonresume

        d = self._none_to_empty_str(d)  # convert NONE values to ""
        d = self._strip_value(d)  # remove any leading/training whitespace from values
        try:
            # print(f"d: {d}")
            d = self._union_jsonresume(d)
            d = self._normalize_jsonresume(d)
            is_valid_json = True
            validate = JRValidate()
            # is_valid_jsonresume = validate.is_valid_json_resume(d)
            # is_valid_jsonresume = True
            # print()
            #     try:
            outdata = self.conv.normalize_camel_case(d)
            # logger.info("validating jsonschema...")
            is_valid_jsonresume = validate.is_valid_json_resume(outdata)
            # print()
        except:
            logger.error(f"Error normalizing json resume: {json.dumps(d)}")
            # logger.info(json.dumps(d))
            outdata = d

        # is_valid_jsonresume = False


        return outdata, is_valid_json, is_valid_jsonresume

    def _union_jsonresume(self, d):
        jr = {
            "basics": {},
            "work": [],
            "education": [],
            "projects": [],
            "volunteer": [],
            "skills": [],
            "publications": [],
            "languages": [],
            "awards": [],
            "certificates": [],
            "references": [],
            "interests": []
        }
        # add empty properties for any that are missing
        d2 = jr | d
        # remove any empty required sub-objects

        default_location = {
            "city": "",
            "region": "",
            "countrycode": "",
            "address": "",
            "postalcode": ""
        }
        location = d2["basics"].get("location", default_location)
        d2["basics"]["location"] = location if isinstance(location, dict) else default_location
        d2["work"] = self._filter_out_empty(d2, "work")
        d2["education"] = self._filter_out_empty(d2, "education")
        d2["volunteer"] = self._filter_out_empty(d2, "volunteer")
        d2["skills"] = self._filter_out_empty(d2, "skills")
        d2["publications"] = self._filter_out_empty(d2, "publications")
        d2["languages"] = self._filter_out_empty(d2, "languages")
        d2["awards"] = self._filter_out_empty(d2, "awards")
        d2["certificates"] = self._filter_out_empty(d2, "certificates")
        d2["interests"] = self._filter_out_empty(d2, "interests")

        # re-order properties in Jsonresume object to maintain desired order
        return {
            "basics": d2["basics"],
            "work": d2["work"],
            "education": d2["education"],
            "projects": d2["projects"],
            "volunteer": d2["volunteer"],
            "skills": d2["skills"],
            "publications": d2["publications"],
            "languages": d2["languages"],
            "awards": d2["awards"],
            "certificates": d2["certificates"],
            "references": d2["references"],
            "interests": d2["interests"],
        }

    def _filter_out_empty(self, d, name):
        obj_list = d[name]
        return [x for x in obj_list if x]

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
        if isinstance(obj, str):
            if obj == "None":
                return ""
            return obj.strip()
        return obj




    def _str_to_dict(self, d):
        list_atts = ["profiles", "highlights", "roles", "keywords"]

        for k in list_atts:
            if k in d:
                if d[k] == "":
                    d[k] = []
        return d



    def _normalize_jsonresume(self, d):

        default_basics = {"name": "", "label": "", "email": "", "website": "", "phone": "", "url": "", "summary": "",
                          "location": {}, "profiles": []}
        d["basics"] = default_basics | d["basics"]
        d["basics"]["phone"] = str(d["basics"]["phone"])
        # d["basics"] = self._str_to_dict(d)
        default_location = {"city": "", "region": "", "address": "", "postalCode": "", "countryCode": ""}
        d["basics"]["location"] = default_location | d["basics"]["location"]
        default_profile = {"url": "", "network": "", "username": ""}
        d["basics"]["profiles"] = [default_profile | p for p in d["basics"]["profiles"]]


        default_work = {"name": "", "position": "", "url": "", "location": "", "startDate": "", "endDate": "",
                        "summary": "", "description": "",  "highlights": []}
        d["work"] = [default_work | x for x in d["work"]]
        d["work"] = [self._str_to_dict(x) for x in d["work"]]

        default_education = {"institution": "", "url": "", "area": "", "studyType": "", "startDate": "", "endDate": "",
                             "score": "", "minors": [],  "courses": []}
        d["education"] = [default_education | x for x in d["education"]]

        default_project = {"name": "", "startDate": "", "endDate": "", "url": "", "description": "", "roles": [], "highlights": []}
        d["projects"] = [default_project | x for x in d["projects"]]
        d["projects"] = [self._str_to_dict(x) for x in d["projects"]]

        default_volunteer = {"organization": "", "position": "", "url": "", "startDate": "", "endDate": "",
                             "summary": "", "highlights": []}
        d["volunteer"] = [default_volunteer | x for x in d["volunteer"]]

        default_skills = {"name": "", "level": "", "keywords": []}
        d["skills"] = [default_skills | x for x in d["skills"]]
        d["skills"] = [self._str_to_dict(x) for x in d["skills"]]


        default_publication = {"name": "", "publisher": "", "releaseDate": "", "url": "", "summary": ""}
        d["publications"] = [default_publication | x for x in d["publications"]]

        default_language = {"language": "", "fluency": ""}
        d["languages"] = [default_language | x for x in d["languages"]]

        default_award = {"title": "", "date": "", "awarder": "", "summary": ""}
        d["awards"] = [default_award | x for x in d["awards"]]

        default_certificate = {"date": "", "name": "", "issuer": "", "url": ""}
        d["certificates"] = [default_certificate | x for x in d["certificates"]]

        default_reference = {"name": "", "reference": ""}
        d["references"] = [default_reference | x for x in d["references"]]

        default_interest = {"name": ""}
        d["interests"] = [default_interest | x for x in d["interests"]]
        return d