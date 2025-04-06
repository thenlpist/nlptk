import json
import os
import unittest
from pathlib import Path


from nlptk import PostProcess


class TestStringMethods(unittest.TestCase):

    def test_json_fixer(self):
        fo = open("response1.json")
        json_str = fo.read()
        fo.close()
        pp = PostProcess()
        result, is_valid_json, is_valid_jsonresume = pp.postprocess(json_str)
        print()
        print(f"is_valid_json:        {is_valid_json}")
        print(f"is_valid_jsonresume:  {is_valid_jsonresume}")
        print()
        print(json.dumps(result, indent=2))

    def test_all(self):
        data_dir = Path("/Users/chagerman/Data/Jobscan/Resumes/QA_Test_20250404/out")
        paths = [data_dir.joinpath(p) for p in os.listdir(data_dir)]
        for path in paths:
            print(f"processing {path}")
            with open(path) as fo:
                txt = fo.read()
            d = json.loads(txt)
            json_str = d["jsonresume"]
            statuscode = d["statuscode"]
            pp = PostProcess()
            result, is_valid_json, is_valid_jsonresume = pp.postprocess(json_str)
            print(f"original statuscode:  {statuscode}")
            print(f"name:                 {result['basics']['name']}")
            print(f"is_valid_json:        {is_valid_json}")
            print(f"is_valid_jsonresume:  {is_valid_jsonresume}")
            print("-" * 80)
            assert is_valid_jsonresume == True


if __name__ == '__main__':
    unittest.main()
