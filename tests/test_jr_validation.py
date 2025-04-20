import json
import unittest

from nlptk import JRValidate


class TestJRValidation(unittest.TestCase):

    def test_validation(self):
        valid = JRValidate()
        # d = json.loads(self.raw_response)
        data = json.loads(open("/Users/chagerman/Data/Jobscan/Resumes/samples/sample_parser_response.json").read())
        d = data["jsonresume"]
        is_valid_jsonresume = valid.is_valid_json_resume(d)

        print()
        print(f"is_valid_jsonresume:  {is_valid_jsonresume}")
        print()


if __name__ == '__main__':
    unittest.main()
