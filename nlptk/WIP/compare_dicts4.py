def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.

    Args:
        s1 (str): First string
        s2 (str): Second string

    Returns:
        int: The Levenshtein distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def compare_dicts(dict1, dict2, threshold=3):
    """
    Recursively compare two nested dictionaries.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary
        threshold (int): Maximum Levenshtein distance to consider strings similar

    Returns:
        dict: A comparison report with the following structure:
            {
                'matching_keys': int,
                'missing_keys': list,
                'extra_keys': list,
                'matching_values': int,
                'different_values': list of tuples (key, value1, value2, distance),
                'similar_values': list of tuples (key, value1, value2, distance)
            }
    """
    result = {
        'matching_keys': 0,
        'missing_keys': [],
        'extra_keys': [],
        'matching_values': 0,
        'different_values': [],
        'similar_values': []
    }

    # Find keys in dict1 but not in dict2
    for key in dict1:
        if key not in dict2:
            result['missing_keys'].append(key)

    # Find keys in dict2 but not in dict1
    for key in dict2:
        if key not in dict1:
            result['extra_keys'].append(key)

    # Compare values for common keys
    for key in dict1:
        if key in dict2:
            result['matching_keys'] += 1
            value1 = dict1[key]
            value2 = dict2[key]

            # Case 1: Both values are dictionaries, recurse
            if isinstance(value1, dict) and isinstance(value2, dict):
                sub_result = compare_dicts(value1, value2, threshold)

                # Merge results
                result['matching_keys'] += sub_result['matching_keys']
                result['missing_keys'].extend([f"{key}.{k}" for k in sub_result['missing_keys']])
                result['extra_keys'].extend([f"{key}.{k}" for k in sub_result['extra_keys']])
                result['matching_values'] += sub_result['matching_values']
                result['different_values'].extend([(f"{key}.{k}", v1, v2, d) for k, v1, v2, d in sub_result['different_values']])
                result['similar_values'].extend([(f"{key}.{k}", v1, v2, d) for k, v1, v2, d in sub_result['similar_values']])

            # Case 2: Both values are strings, compare with Levenshtein
            elif isinstance(value1, str) and isinstance(value2, str):
                distance = levenshtein_distance(value1, value2)
                if distance == 0:
                    result['matching_values'] += 1
                elif distance <= threshold:
                    result['similar_values'].append((key, value1, value2, distance))
                else:
                    result['different_values'].append((key, value1, value2, distance))

            # Case 3: Mixed types, count as different
            else:
                result['different_values'].append((key, value1, value2, -1))

    return result

# Example usage
if __name__ == "__main__":
    dict1 = {
        "person": {
            "name": "John Doe",
            "address": {
                "street": "123 Main St",
                "city": "Anytown"
            }
        },
        "contact": "john@example.com"
    }

    dict2 = {
        "person": {
            "name": "John Doe",
            "address": {
                "street": "123 Main Street",
                "city": "Any Town"
            }
        },
        "contact": "john@examples.com"
    }

    comparison = compare_dicts(dict1, dict2, threshold=3)

    print("Comparison Results:")
    print(f"Matching keys: {comparison['matching_keys']}")
    print(f"Missing keys: {comparison['missing_keys']}")
    print(f"Extra keys: {comparison['extra_keys']}")
    print(f"Matching values: {comparison['matching_values']}")
    print("\nDifferent values:")
    for key, val1, val2, distance in comparison['different_values']:
        print(f"  {key}: '{val1}' vs '{val2}' (distance: {distance})")
    print("\nSimilar values:")
    for key, val1, val2, distance in comparison['similar_values']:
        print(f"  {key}: '{val1}' vs '{val2}' (distance: {distance})")