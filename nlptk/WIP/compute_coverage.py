import re
import json
import os
from pathlib import Path

"""
Desired behavior
- compute coverage (how much of resume text was accurately extracted)
- label each leaf value with (1) whether it is a match (or closeness score?) and
    (2) whether that value is empty ("")
- it might also be useful to note the line number the value was found on
    and maybe the text index within that line (later addition)
    n.b. this could be useful in checking that adjacent values are near each other.
    Could also be used to identify the "other" section daniel wants. 
    Could also be used to infer section headings maybe 
e.g. 
    "phone": {
      "value": "555-1234",
      "similarity": 1.0,
      "has_match": true,
      "is_empty": false
      "line_no": 3
    }



"""


def main(data):

    text = clean(data["text"])
    # text = data["text"]
    print(f"parser: {data['parser']}")
    text_len = len(text)
    jsonresume = data["jsonresume"]
    print(json.dumps(jsonresume, indent=2))

    text2 = remove_extracted(jsonresume, text)
    text2 = re.sub("^- ", "", text2)
    text2_len = len(text2)

    print()
    print(text2)
    print()
    print(f"text_len: {text_len}  text2_len: {text2_len}  {text2_len}/{text_len}  ({(text2_len / text_len):.2f}%) ")




def remove_extracted(obj, text):
    """Recursive function to compute coverage of extracted JSON data"""

    if isinstance(obj, list):
        for item in obj:
            text = remove_extracted(item, text)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            text = remove_extracted(v, text)
    else:
        text = sub_text(obj, text)
    return text


def clean(s):
    return re.sub(r"[\+\(\)\[\]\{\}]", "", s)

def sub_text(s, text):
    if s:
        text2 = re.sub(clean(s), "", text)
        return text2
    return text


def flatten(obj):
    """Recursive function to remove outer "value" from dicts"""
    if isinstance(obj, list):
        return [flatten(v) for v in obj]
    elif isinstance(obj, dict):
        if list(obj.keys()) == ["value"]:
            return flatten(obj["value"])
        return {k.lower(): flatten(v) for k, v in obj.items()}
    else:
        return obj




if __name__ == "__main__":
    home = Path.home()
    sample_path = home.joinpath("Data/Jobscan/Resumes/samples/sample_parser_response.json")
    data = json.loads(open(sample_path).read())
    main(data)
