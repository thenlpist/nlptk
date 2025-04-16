import json

import Levenshtein


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


def compare_dicts(dict1, dict2, threshold=0.8):
    """
    Recursively compare two nested dictionaries.
    String values are compared using Levenshtein distance with a similarity threshold.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary
        threshold (float): Similarity threshold (0 to 1) for string comparisons

    Returns:
        dict: Dictionary containing comparison results
    """

    result = {}
    print(f"          type(dict1): {type(dict1)}  type(dict2): {type(dict2)} ")
    # Get all keys from both dictionaries
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    # print(f"type(dict1): {type(dict1)}  type(dict2): {type(dict2)} all_keys: {all_keys}")
    print(f"all_keys: {all_keys} ")


    for key in all_keys:
        # Handle keys present in only one dictionary
        if key not in dict1:
            result[key] = {"status": "missing_in_dict1", "value_dict2": dict2[key]}
            continue
        if key not in dict2:
            result[key] = {"status": "missing_in_dict2", "value_dict1": dict1[key]}
            continue

        value1 = dict1[key]
        value2 = dict2[key]

        # Handle nested dictionaries recursively
        if isinstance(value1, dict) and isinstance(value2, dict):
            result[key] = compare_dicts(value1, value2, threshold)

        # Handle string comparison using Levenshtein distance
        elif isinstance(value1, str) and isinstance(value2, str):
            # Calculate Levenshtein distance
            distance = Levenshtein.distance(value1, value2)
            max_len = max(len(value1), len(value2))

            # Convert distance to similarity ratio (0 to 1)
            if max_len == 0:  # Both strings are empty
                similarity = 1.0
            else:
                similarity = 1.0 - (distance / max_len)

            result[key] = {
                "value1": value1,
                "value2": value2,
                "similarity": similarity,
                "match": similarity >= threshold
            }

        # Handle type mismatch
        elif type(value1) != type(value2):
            result[key] = {
                "status": "type_mismatch",
                "type1": type(value1).__name__,
                "type2": type(value2).__name__,
                "value1": value1,
                "value2": value2
            }


        elif isinstance(value1, list) and isinstance(value2, list):
            if isinstance(value1[0], dict) and isinstance(value2[0], dict):
                result[key] = [compare_dicts(v1, v2, threshold) for v1, v2 in zip(value1, value2)]
            elif isinstance(value1[0], str) and isinstance(value2[0], str):
                result[key] = [compute_similarity_result(s1, s2, threshold) for s1, s2 in zip(value1, value2)]

        # Handle other value types (not dictionaries or strings)
        else:
            result[key] = {
                "status": "unsupported_type",
                "type": type(value1).__name__,
                "value1": value1,
                "value2": value2,
                "match": value1 == value2
            }

    return result



def compute_similarity_result(s1, s2, threshold):
    distance = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))

    # Convert distance to similarity ratio (0 to 1)
    if max_len == 0:  # Both strings are empty
        similarity = 1.0
    else:
        similarity = 1.0 - (distance / max_len)

    return {
        "value1": s1,
        "value2": s2,
        "similarity": similarity,
        "match": similarity >= threshold
    }


# Example usage
if __name__ == "__main__":
    # Sample nested dictionaries
    dict1 = {
        "personal": {
            "name": "John Smith",
            "email": "john.smith@example.com"
        },
        "address": {
            "street": "123 Main Street",
            "city": "New York",
            "zip": "10001",
            "country": {
                "name": "USA",
                "countrycode": "US"
            }
        },
        "profiles": [{
            "network": "Linkedin",
            "url": "http://www.linkedin.com/johnsmith"
        }]
    }

    dict2 = {
        "personal": {
            "name": "Jon Smith",  # Slightly different
            "email": "john.smith@example.com",
            "phone": "555-1234"  # Additional field
        },
        "address": {
            "street": "123 Main St",  # Abbreviated
            "city": "New York",
            "zip": "10001",
            "country": {
                "name": "America",
                "countrycode": "US"
            }
        },
        "profiles": [{
            "network": "Linkedin",
            "url": "http://www.linkedin.com/johnsmith"
        }]
    }

    dict3 = {
        "basics": {
            "name": "Jane Doe",
            "label": "Sales Executive",
            "phone": "555-1234",
            "summary": "Dynamic and results-driven Sales Executive with over 10 years of experience.",
            "location": {"city": "London",
                         "address": "123 forth st",
                         "postalCode": "12345",
                         "countryCode": "UK"},
        },
        "work": [
            {
                "name": "Media Plus",
                "position": "Junior Sales Executive",
                "startDate": "2012-06",
                "endDate": "2013-12",
                "summary": "Supported senior sales team members in prospecting new clients and maintaining existing accounts.",
                "highlights": ["Assisted in preparing sales presentations.",
                               "Achieved 100% of personal sales targets."]
            }
        ]
    }



    dict4 = {
        "basics": {
            "name": "Jane Doe",
            "label": "Sales Executive",
            "phone": "555-1234",
            "summary": "Dynamic and results-driven Sales Executive with over 10 years of experience.",

            "location": {"city": "London",
                         "address": "123 forth st",
                         "postalCode": "12345",
                         "countryCode": "UK"},
        },
        "work": [
            {
                "name": "Media Plus",
                "position": "Junior Sales Executive",
                "startDate": "2012-06",
                "endDate": "2013",
                "summary": "Supported senior sales team members in prospecting new clients and maintaining existing accounts.",
                "highlights": ["Assisted in preparing sales presentations.",
                               "Achieved 100 of personal sales targets."]
            }
        ]
    }



    # Compare dictionaries
    result = compare_dicts(dict3, dict4)

    # Print results in a readable format

    print(json.dumps(result, indent=2))
