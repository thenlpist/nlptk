import json
import unittest

from nlptk import PostProcess
import base64
import json
from dataclasses import dataclass
from pathlib import Path

import requests

PORT = "8001"
HOSTNAME = "10.0.0.105"
BASE_URL = f"http://{HOSTNAME}:{PORT}"

@dataclass
class Endpoint:
    hello = f"{BASE_URL}/hello"
    static = f"{BASE_URL}/static"
    parse_resume_text = f"{BASE_URL}/parse_resume"
    parse_resume_doc = f"{BASE_URL}/parse_resume_doc"



class TestResumePostProcessing(unittest.TestCase):

    def test_hello(self):
        url = f"{BASE_URL}/hello"
        response = requests.get(Endpoint.hello)
        # print(response)
        # print(json.dumps(response.json(), indent=2))
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello, World!"}


    def test_raw_resume(self):
        pp = PostProcess()
        url = f"{BASE_URL}/raw_parse_resume_doc"
        print(f"URL: {url}")
        cwd = Path.cwd()
        resources_dir = cwd.joinpath("resources")
        resume_path = resources_dir.joinpath("resumes/resume_1.docx")
        assert resume_path.exists()

        filename = resume_path.name
        with open(resume_path, "rb") as fo:
            encoded_string = base64.b64encode(fo.read())
        payload = {"filename": filename, "filedata": encoded_string}
        raw_response = requests.post(url=url, data=payload)
        # print(raw_response)
        # print(json.dumps(raw_response.json()["jsonresume"], indent=2))
        parser_response = json.dumps(raw_response.json()["jsonresume"])
        d, is_valid_json, is_valid_jsonresume = pp.postprocess(parser_response)
        print("-" * 80)
        print(f"is_valid_json: {is_valid_json},  is_valid_jsonresume: {is_valid_jsonresume}")
        print("-" * 80)
        print(raw_response.json()["text"])
        print("-" * 80)
        print(json.dumps(d, indent=2))


    def test_resume(self):
        # pp = PostProcess()
        url = f"{BASE_URL}/parse_resume_doc"
        print(f"URL: {url}")
        cwd = Path.cwd()
        resources_dir = cwd.joinpath("resources")
        resume_path = resources_dir.joinpath("resumes/resume_1.docx")
        assert resume_path.exists()

        filename = resume_path.name
        with open(resume_path, "rb") as fo:
            encoded_string = base64.b64encode(fo.read())
        payload = {"filename": filename, "filedata": encoded_string}
        raw_response = requests.post(url=url, data=payload)
        d = raw_response.json()
        assert d["statuscode"] == 200
        assert d["statuscode"] == 200
        assert d["is_valid_json"] == True
        assert d["is_valid_jsonresume"] == True
        # print(json.dumps(raw_response.json()["jsonresume"], indent=2))
        print(json.dumps(d, indent=2))
        # print(raw_response.json()["text"])


if __name__ == '__main__':
    unittest.main()
