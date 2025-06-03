from pathlib import Path
import json
import unittest

from nlptk import JRValidate


class TestJRValidation(unittest.TestCase):

    def test_validation(self):
        valid = JRValidate()
        # d = json.loads(self.raw_response)
        cwd = Path.cwd()
        resources_dir = cwd.joinpath("resources")
        sample_path = resources_dir.joinpath("sample_parser_response.json")
        data = json.loads(open(sample_path).read())
        d = data["jsonresume"]
        is_valid_jsonresume = valid.is_valid_json_resume(d)

        print()
        print(f"is_valid_jsonresume:  {is_valid_jsonresume}")
        print()


if __name__ == '__main__':
    unittest.main()
