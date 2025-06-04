import copy
import logging
import re
from typing import Optional
from typing import Union

import json_repair

from nlptk.jrprocessor.jr_validation import JRValidate
from nlptk.jrprocessor.regex_patterns import RegexPatterns as pat
from nlptk.jsonresume.converter import Converter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create file handler that logs debug and higher level messages
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)


class PostProcess:
    def __init__(self, parser_version=""):
        self.parser_version = parser_version
        self.conv = Converter()

    def postprocess(self, raw_response: Union[str, dict]):
        # logger.info(f"type(raw_response): {type(raw_response)}")
        d: dict = self._coerce_to_json(raw_response)
        is_valid_json = False
        is_valid_jsonresume = False
        if not d:
            return raw_response, is_valid_json, is_valid_jsonresume
        d = self.conv.flatten(d)
        d = self.conv.filter_out_keys(d)
        d = self._none_to_empty_str(d)  # convert NONE values to ""
        d = self._strip_value(d)  # remove any leading/training whitespace from values

        try:
            d = self._union_jsonresume(d)
            d = self._normalize_jsonresume(d)
            is_valid_json = True
            validate = JRValidate()
            d = self.conv.normalize_camel_case(d)
            d = self._reformat_dates(d)
            outdata = self.conv.reorder_all_sections(d)
            is_valid_jsonresume = validate.is_valid_json_resume(outdata)

        except:
            logger.error(f"Error normalizing json resume for resume id: {d['id']}")
            outdata = d
        return outdata, is_valid_json, is_valid_jsonresume

    # --------------------------------------------------------------------------------
    # Coerce raw string response into a JSON object if possible. Try to "save" JSON where possible.
    # --------------------------------------------------------------------------------
    def _coerce_to_json(self, raw_response: str) -> Optional[dict]:
        if isinstance(raw_response, str):
            parser_response = self._strip_bad_chars(raw_response)
            response = self._clean_response(copy.copy(parser_response))
            d = json_repair.loads(response)
        elif isinstance(raw_response, dict):
            d = raw_response
        else:
            raise ValueError(f"_coerce_to_json argument must be either a str or dict. Argument type: {type(raw_response)}")
        if isinstance(d, list):
            if len(d) == 0:
                return None
            else:
                d = self._coerce_to_json(d[0])
        if isinstance(d, dict):
            return d
        return None

    # --------------------------------------------------------------------------------
    # Post-processing. Strip out bad unicode-ish characters that are generated
    # --------------------------------------------------------------------------------
    def _strip_bad_chars(self, returned_text):
        pat1 = re.compile(" ?(u2202|u00a0|u00a),? ?")
        pat2 = re.compile(r"\b(t )+")
        t = pat1.sub("", returned_text)
        t = pat2.sub("", t)
        t = re.sub(r"\\ t", "", t)
        t = re.sub(r"\\ ", "", t)
        t = pat.repeat_pat.sub("", t)
        return t

    def _clean_dict_item(self, item, key):
        text = item[key]
        t = re.sub("^- ", "", text)
        t = re.sub(r"\\ t", "", t)
        t = re.sub(r"\\ ", "", t)

        item[key] = t
        return item

    def _clean_work_highlights(self, work_item):
        # check if item is string since it is possible a dict etc was generated instead. sigh!
        work_item["highlights"] = [re.sub("^- ", "", h) for h in work_item["highlights"] if isinstance(h, str)]
        return work_item

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

        basics = d2["basics"]
        d2["basics"] = {} if not isinstance(basics, dict) else basics
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
        profiles = [p for p in d["basics"]["profiles"] if p and isinstance(p, dict)]
        d["basics"]["profiles"] = [default_profile | p for p in profiles]

        default_work = {"name": "", "position": "", "url": "", "location": "", "startDate": "", "endDate": "",
                        "summary": "", "description": "", "highlights": []}
        work = [p for p in d["work"] if p and isinstance(p, dict)]
        d["work"] = [default_work | x for x in work]
        d["work"] = [self._str_to_dict(x) for x in d["work"]]
        d["work"] = [self._clean_work_highlights(w) for w in d["work"]]
        default_education = {"institution": "", "url": "", "area": "", "studyType": "", "startDate": "", "endDate": "",
                             "score": "", "minors": [], "courses": []}
        education = [p for p in d["education"] if p and isinstance(p, dict)]
        d["education"] = [default_education | x for x in education]

        default_project = {"name": "", "startDate": "", "endDate": "", "url": "", "description": "", "roles": [],
                           "highlights": []}
        projects = [p for p in d["projects"] if p and isinstance(p, dict)]
        d["projects"] = [default_project | x for x in projects]
        d["projects"] = [self._str_to_dict(x) for x in d["projects"]]

        default_volunteer = {"organization": "", "position": "", "url": "", "startDate": "", "endDate": "",
                             "summary": "", "highlights": []}
        volunteer = [p for p in d["volunteer"] if p and isinstance(p, dict)]
        d["volunteer"] = [default_volunteer | x for x in volunteer]

        default_skills = {"name": "", "level": "", "keywords": []}
        d["skills"] = [default_skills | x for x in d["skills"]]
        d["skills"] = [self._str_to_dict(x) for x in d["skills"]]
        d["skills"] = [self._clean_dict_item(x, "name") for x in d["skills"]]

        default_publication = {"name": "", "publisher": "", "releaseDate": "", "url": "", "summary": ""}
        publications = [p for p in d["publications"] if p and isinstance(p, dict)]
        d["publications"] = [default_publication | x for x in publications]

        default_language = {"language": "", "fluency": ""}
        languages = [p for p in d["languages"] if p and isinstance(p, dict)]
        d["languages"] = [default_language | x for x in languages]

        default_award = {"title": "", "date": "", "awarder": "", "summary": ""}
        awards = [p for p in d["awards"] if p and isinstance(p, dict)]
        d["awards"] = [default_award | x for x in awards]

        default_certificate = {"date": "", "name": "", "issuer": "", "url": ""}
        certificates = [p for p in d["certificates"] if p and isinstance(p, dict)]
        d["certificates"] = [default_certificate | x for x in certificates]

        default_reference = {"name": "", "reference": ""}
        references = [p for p in d["references"] if p and isinstance(p, dict)]
        d["references"] = [default_reference | x for x in references]

        default_interest = {"name": ""}
        interests = [p for p in d["interests"] if p and isinstance(p, dict)]
        d["interests"] = [default_interest | x for x in interests]
        return d

    def _reformat_dates(self, obj):
        """Recursive function to reformat date strings from YYYY-MM-DD to YYYY-MM"""
        date_keys = ["startdate", "enddate", "date", "releasedate", "startDate", "endDate", "date", "releaseDate"]
        if isinstance(obj, list):
            return [self._reformat_dates(v) for v in obj]
        elif isinstance(obj, dict):
            for k in date_keys:
                if k in obj:
                    date_string = obj[k]
                    if not date_string == "":
                        obj[k] = re.sub("([0-9]{4}-[0-9]{2})-[0-9]{2}", r"\1", date_string)
            return {k: self._reformat_dates(v) for k, v in obj.items()}
        else:
            return obj
