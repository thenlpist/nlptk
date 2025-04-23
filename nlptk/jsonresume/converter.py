class Converter:

    def normalize_camel_case(self, d: dict) -> dict:
        """ Receive a dict containing almost-valid JSONResume data
            Normalize by converting all relevant keys to camelCase
            n.b. This is useful for model predictions that use lower-case keys as a result of being
            trained on the `data` object.
        """
        # d = self.filter_for_valid_schema(d) # unnecessary since later functions do the same
        d = self.flatten(d)
        d = self.to_camelcase(d)
        d = self.filter_out_keys(d)
        return self.reorder_all_sections(d)

    def filter_for_valid_schema(self, d):
        """ Remove extraneous sections in JSON data such as:
            ["fileinfo", "formatting", "sectionheadings", "additional", "categorizedskills", "categorizedskills_1_", "categorizedskills_0_"]
         """
        return {
            "basics": d["basics"],
            "work": d.get("work", []),
            "education": d.get("education", []),
            "projects": d.get("projects", []),
            "volunteer": d.get("volunteer", []),
            "skills": d.get("skills", []),
            "publications": d.get("publications", []),
            "languages": d.get("languages", []),
            "awards": d.get("awards", []),
            "certificates": d.get("certificates", []),
            "references": d.get("references", []),
            "interests": d.get("interests", []),
        }

    def to_camelcase(self, obj):
        """Recursive function to convert relevant keys to camelCase"""

        def get_key(k):
            """ define a dict for converting lowercase to camelCase """
            low2cc = {"startdate": "startDate",
                      "enddate": "endDate",
                      "releasedate": "releaseDate",
                      "studytype": "studyType",
                      "postalcode": "postalCode",
                      "countrycode": "countryCode"}
            newkey = low2cc.get(k, k)
            return newkey

        if isinstance(obj, list):
            return [self.to_camelcase(v) for v in obj]
        elif isinstance(obj, dict):
            return {get_key(k): self.to_camelcase(v) for k, v in obj.items()}
        else:
            return obj

    def flatten(self, obj):
        """Recursive function to remove outer "value" from dicts"""
        if isinstance(obj, list):
            return [self.flatten(v) for v in obj]
        elif isinstance(obj, dict):
            if list(obj.keys()) == ["value"]:
                return self.flatten(obj["value"])
            return {k.lower(): self.flatten(v) for k, v in obj.items()}
        else:
            return obj

    def filter_out_keys(self, d):
        """ Recursive function to remove unwanted/unnecessary keys from a `data` object """
        keys_to_remove = {"meta", "uuid", "image", "highlights__re", "a_nrea",
                          "courses__st", "minors__st", "selected"}
        d2 = dict()
        for key in d:
            if key in keys_to_remove:
                pass  # ignore meta keys
            else:
                entry = d[key]
                if isinstance(entry, dict):
                    if key in keys_to_remove:
                        pass
                    else:
                        d2[key] = self.filter_out_keys(d[key])
                elif isinstance(entry, list):
                    d2[key] = []
                    for item in entry:
                        if isinstance(item, dict):
                            d2[key].append(self.filter_out_keys(item))
                        else:
                            d2[key].append(item)
                else:
                    d2[key] = d[key]
        return d2

    def reorder_all_sections(self, d):
        """ Make sure that each section of a JSON resume follows the canonical order for that section. """
        # default_basics = {"name": "", "label": "", "email": "", "website": "", "phone": "", "url": "", "summary": "",
        #                   "location": {}, "profiles": []}
        # basics = self.reorder_section(d.get("basics", []), default_basics)

        default_basics = {"name": "", "label": "", "email": "", "website": "", "phone": "", "url": "", "summary": "",
                          "location": {}, "profiles": []}
        basics = default_basics | d["basics"]
        basics["phone"] = str(basics["phone"])

        # d["basics"] = self._str_to_dict(d)
        default_location = {"city": "", "region": "", "address": "", "postalCode": "", "countryCode": ""}
        d["basics"]["location"] = default_location | d["basics"]["location"]
        default_profile = {"url": "", "network": "", "username": ""}
        d["basics"]["profiles"] = [default_profile | p for p in d["basics"]["profiles"]]

        default_work = {"name": "", "position": "", "url": "", "location": "", "startDate": "", "endDate": "",
                        "summary": "", "highlights": []}
        work = [self.reorder_section(x, default_work) for x in d.get("work", [])]
        # default_education = {"institution": "", "url": "", "area": "", "studyType": "", "startDate": "", "endDate": "",
        #                      "score": "", "courses": []}
        # education = [self.reorder_section(x, default_education) for x in d.get("education", [])]


        default_education = {"institution": "", "url": "", "area": "", "studyType": "", "startDate": "", "endDate": "",
                             "score": "", "minors": [],  "courses": []}
        education = [default_education | x for x in d["education"]]

        default_project = {"name": "", "startDate": "", "endDate": "", "url": "", "description": "", "roles": [], "highlights": []}
        projects = [self.reorder_section(x, default_project) for x in d.get("projects", [])]
        default_volunteer = {"organization": "", "position": "", "url": "", "startDate": "", "endDate": "",
                             "summary": "", "highlights": []}
        volunteer = [self.reorder_section(x, default_volunteer) for x in d.get("volunteer", [])]
        default_skills = {"name": "", "level": "", "keywords": []}
        skills = [self.reorder_section(x, default_skills) for x in d.get("skills", [])]
        default_publication = {"name": "", "publisher": "", "releaseDate": "", "url": "", "summary": ""}
        publications = [self.reorder_section(x, default_publication) for x in d.get("publications", [])]
        default_language = {"language": "", "fluency": ""}
        languages = [self.reorder_section(x, default_language) for x in d.get("languages", [])]
        default_award = {"title": "", "date": "", "awarder": "", "summary": ""}
        awards = [self.reorder_section(x, default_award) for x in d.get("awards", [])]
        default_certificate = {"date": "", "name": "", "issuer": "", "url": ""}
        certificates = [self.reorder_section(x, default_certificate) for x in d.get("certificates", [])]
        default_reference = {"name": "", "reference": ""}
        references = [self.reorder_section(x, default_reference) for x in d.get("references", [])]
        default_interest = {"name": ""}
        interests = [self.reorder_section(x, default_interest) for x in d.get("interests", [])]

        return {
            "basics": basics,
            "work": work,
            "education": education,
            "projects": projects,
            "volunteer": volunteer,
            "skills": skills,
            "publications": publications,
            "languages": languages,
            "awards": awards,
            "certificates": certificates,
            "references": references,
            "interests": interests
        }

    def reorder_section(self, d: dict, default: dict):
        """ Return a given resume section (1) in the canonical order and with (2) extraneous attributes removed """
        jr = default | d
        return {k: jr.get(k, None) for k in default.keys()}
