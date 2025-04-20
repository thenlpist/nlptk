import json
import re
from pathlib import Path

import Levenshtein
from rollup_compare_dicts import *

def rollup_scores(dictionary):
    pass



def compare_dict_to_text(dictionary, text, approach="default", threshold=0.8):
    """
    Recursively compare a nested dictionary's leaf string values to a text document.
    For each leaf value, search for that string in the document.
    Remove matched strings from the document.

    Args:
        dictionary (dict): A nested dictionary with string leaf values
        text (str): The text document to search in
        approach (str): one of {levenshtein, regex, default} to determine matching and replacing approach
        threshold (float): Similarity threshold for Levenshtein matching (if enabled)

    Returns:
        tuple: (result_dict, updated_text_document)
            - result_dict: Dictionary with match information
            - updated_text_document: Text with matched strings removed
    """

    result = {}

    updated_text = clean_text(text)

    def process_dict(current_dict, parent_key=""):
        nonlocal updated_text
        result_dict = {}

        for key, value in current_dict.items():
            current_key = f"{parent_key}.{key}" if parent_key else key

            # Handle nested dictionaries recursively
            if isinstance(value, dict):
                result_dict[key] = process_dict(value, current_key)

            elif isinstance(value, list):
                if not value:
                    result_dict[key] = {
                        "value": value,
                        "similarity": 0.0,
                        "match": False,
                        "is_empty": True
                    }
                elif isinstance(value[0], dict):
                    result_dict[key] = [process_dict(v, current_key) for v in value]
                elif isinstance(value[0], str):
                    result_list = []
                    for v in value:
                        obj, updated_text = compute_coverage(v, updated_text, approach, threshold)
                        result_list.append(obj)
                    result_dict[key] = result_list

            # Handle string values - search in the text document
            elif isinstance(value, str):
                # Skip empty strings
                if not value.strip():
                    result_dict[key] = {
                        "value": value,
                        "similarity": 0.0,
                        "match": False,
                        "is_empty": True
                    }
                    continue

                result_dict[key], updated_text = compute_coverage(value, updated_text, approach, threshold)

            else:
                # Handle non-string, non-dict values
                result_dict[key] = {
                    "status": "not_a_string",
                    "type": type(value).__name__,
                    "value": str(value)
                }

        return result_dict

    # Process the dictionary
    result = process_dict(dictionary)

    return result, updated_text




# def clean_plus(s):
#     return re.sub(r"[\+]", "\\+", s)

def clean_text(s):
    # s = re.sub(r"[\+]", "\\+", s)
    s = s.replace("\xa0", " ")
    s = re.sub(r"[,:\*\+\(\)\[\]\{\}]", "", s)
    # s = re.sub(r"[,:\*\(\)\[\]\{\}]", "", s)
    s = re.sub(" ?## ?", "", s)
    s = re.sub("[\n ][-–] ?", "", s)
    return s


def post_clean(s):
    s = re.sub("\n[\n ]+", "\n", s)
    s = re.sub(
        r"\b(Email|Name|Linkedin|Education|Certifications|Projects|Interests|Professional Summary|Professional Experience|Name|Phone)(?!\.)",
        "", s, flags=re.IGNORECASE)
    s = re.sub("\n\n+", "\n", s)
    return s


def compute_coverage(value, updated_text, approach, threshold):
    match approach:
        case "levenshtein":
            result, updated_text = levenshtein_replace(value, updated_text, threshold)
        case "regex":
            result, updated_text = regex_replace(value, updated_text)
        case _:
            result, updated_text = string_replace(value, updated_text)
    return result, updated_text


def levenshtein_replace(value, updated_text, threshold):
    # For Levenshtein, we need to check each word/phrase in the document
    words = updated_text.split()
    best_match = None
    best_similarity = 0
    best_index = -1

    for i, word in enumerate(words):
        distance = Levenshtein.distance(value, word)
        max_len = max(len(value), len(word))
        similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = word
            best_index = i

    if best_similarity >= threshold:
        # Remove the matched word
        words.pop(best_index)
        updated_text = " ".join(words)
        # result_dict[key] =
        result = {
            "value": value,
            "similarity": best_similarity,
            "match": True,
            "matched_text": best_match,
            "is_empty": False
        }
    else:
        # result_dict[key] =
        result = {
            "value": value,
            "similarity": best_similarity,
            "match": False,
            "best_candidate": best_match,
            "best_similarity": best_similarity,
            "is_empty": False
        }
    return result, updated_text


def regex_replace(value, updated_text):

    # print(value)
    term = clean_text(value.strip())
    # term = re.escape(value)

    if len(term) <= 2:
        pat = re.compile(fr"\b({term})\b")
    else:
        # print(value)
        pat = re.compile(term)
    m = pat.search(updated_text)
    if m:
        updated_text = pat.sub("", updated_text, count=1)
        result = {
            "value": value,
            "similarity": 1.0,
            "match": True,
            "is_empty": False
        }
    else:
        result = {
            "value": value,
            "similarity": 0.0,
            "match": False,
            "is_empty": False
        }
    return result, updated_text


def string_replace(value, updated_text):
    if value in updated_text:
        # Remove the matched string
        updated_text = updated_text.replace(value, "", 1)  # Remove only first occurrence
        # result_dict[key] =
        result = {
            "value": value,
            "similarity": 1.0,
            "match": True,
            "is_empty": False
        }
    else:
        # result_dict[key] = {
        result = {
            "value": value,
            "similarity": 0.0,
            "match": False,
            "is_empty": False
        }
    return result, updated_text


# Example usage
if __name__ == "__main__":
    # Sample nested dictionary
    sample_dict = {
        "personal": {
            "name": "John Smith",
            "email": "john.smith@example.com"
        },
        "address": {
            "street": "123 Main Street",
            "city": "New York",
            "zip": "10001"
        }
    }

    # Sample text document
    sample_text = """
    Contact Information:
    John Smith can be reached at john.smith@example.com.
    He lives at 123 Main Street, New York, 10001.
    Please reach out if you have any questions.
    """

    # # Compare dictionary to text
    # result_dict, updated_text = compare_dict_to_text(sample_dict, sample_text)
    #
    # # Print results
    #
    #
    # print("Match Results:")
    # print(json.dumps(result_dict, indent=2))
    # print("\nUpdated Text Document (after removing matches):")
    # print(updated_text)
    # print("="*80)
    #
    # # Example with Levenshtein matching
    # print("\n\nWith Levenshtein matching:")
    # result_dict_lev, updated_text_lev = compare_dict_to_text(sample_dict, sample_text, threshold=0.8,
    #                                                          use_levenshtein=True)
    # print("Match Results:")
    # print(json.dumps(result_dict_lev, indent=2))
    # print("\nUpdated Text Document (after removing matches):")
    # print(updated_text_lev)

    home = Path.home()
    sample_path = home.joinpath("Data/Jobscan/Resumes/samples/sample_parser_response.json")
    data = json.loads(open(sample_path).read())

    text = data["text"]
    jsonresume = data["jsonresume"]

    # approach = "levenshtein"
    approach = "regex"
    # approach = "default"
    result_dict, updated_text = compare_dict_to_text(jsonresume, text, approach)
    out_text = post_clean(updated_text)

    print("Match Results:")
    print(json.dumps(result_dict, indent=2))
    print("\nUpdated Text Document (after removing matches):")
    print("-" * 40)
    print(out_text)
    with open("/Users/chagerman/Downloads/updated_text.txt", "w") as fo:
        fo.write(out_text)
    with open("/Users/chagerman/Downloads/updated_text_dict.json", "w") as fo:
        fo.write(json.dumps(result_dict, indent=2))
    print("-" * 40)

    print("\nCoverage (how much of the resume was extracted:")
    print(f"text length after/before: {len(out_text)} / {len(text)}  ({1 - (len(out_text) / len(text)):.2f}%) ")

    print("=" * 80)

    # Aggregate similarity scores
    aggregated_result = aggregate_similarity(result_dict)
    metrics = aggregated_result["metrics"]
    metrics["input_text_len"] = len(text)
    metrics["extracted_text_len"] = len(text) - len(out_text)
    metrics["remainder_text_len"] = len(out_text)
    metrics["pct_extracted"] = 1 - (len(out_text) / len(text))
    # text length after/before: 869 / 4134  (0.79%)

    # Print results in a readable format
    print(json.dumps(aggregated_result, indent=2))
