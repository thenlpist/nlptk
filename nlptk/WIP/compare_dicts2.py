# Another Claude AI example

def compare_dicts(dict1, dict2, threshold=0.8):
    """
    Recursively compare two nested dictionaries where leaf values are strings.
    String comparisons use Levenshtein distance to calculate similarity.

    Args:
        dict1: First nested dictionary
        dict2: Second nested dictionary
        threshold: Similarity threshold (0.0-1.0) to consider strings as matching

    Returns:
        Dictionary with comparison results:
        {
            'match': bool,  # Overall match status
            'differences': list,  # List of differences found
            'similarity': float  # Overall similarity score (0.0-1.0)
        }
    """
    import Levenshtein

    def calculate_similarity(str1, str2):
        """Calculate string similarity using Levenshtein distance."""
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0

        distance = Levenshtein.distance(str1, str2)
        max_len = max(len(str1), len(str2))
        return 1.0 - (distance / max_len)

    def compare_recursive(d1, d2, path=None):
        """Recursively compare dictionaries and track differences."""
        if path is None:
            path = []

        differences = []
        total_items = 0
        total_similarity = 0.0

        # Check for keys in dict1 not in dict2
        for key in d1:
            total_items += 1
            current_path = path + [key]
            path_str = '.'.join(str(p) for p in current_path)

            if key not in d2:
                differences.append(f"Key '{path_str}' missing in second dictionary")
                continue

            # If both values are dictionaries, recurse
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                sub_result = compare_recursive(d1[key], d2[key], current_path)
                differences.extend(sub_result['differences'])
                total_similarity += sub_result['similarity'] * len(sub_result['all_items'])
                total_items += len(sub_result['all_items']) - 1  # -1 because we already counted this key

            # If both values are strings, compare with Levenshtein
            elif isinstance(d1[key], str) and isinstance(d2[key], str):
                similarity = calculate_similarity(d1[key], d2[key])
                total_similarity += similarity

                if similarity < threshold:
                    differences.append(
                        f"String values differ at '{path_str}': "
                        f"'{d1[key]}' vs '{d2[key]}' (similarity: {similarity:.2f})"
                    )

            # If types don't match
            else:
                differences.append(
                    f"Type mismatch at '{path_str}': "
                    f"{type(d1[key]).__name__} vs {type(d2[key]).__name__}"
                )
                total_similarity += 0  # Consider as no similarity

        # Check for keys in dict2 not in dict1
        for key in d2:
            if key not in d1:
                current_path = path + [key]
                path_str = '.'.join(str(p) for p in current_path)
                differences.append(f"Key '{path_str}' missing in first dictionary")
                total_items += 1

        # Calculate average similarity
        avg_similarity = total_similarity / total_items if total_items > 0 else 0.0

        return {
            'differences': differences,
            'similarity': avg_similarity,
            'all_items': [1] * total_items  # Helper to track total item count for weighted average
        }

    # Perform the comparison
    result = compare_recursive(dict1, dict2)

    # Return final output
    return {
        'match': len(result['differences']) == 0,
        'differences': result['differences'],
        'similarity': result['similarity']
    }


# Example usage
if __name__ == "__main__":
    dict1 = {
        "person": {
            "name": "John Smith",
            "address": {
                "street": "123 Main St",
                "city": "New York"
            }
        },
        "contact": "john@example.com"
    }

    dict2 = {
        "person": {
            "name": "Jon Smyth",
            "address": {
                "street": "123 Main Street",
                "city": "New York"
            }
        },
        "contact": "john@example.com",
        "extra": "something"
    }

    result = compare_dicts(dict1, dict2)
    print(f"Match: {result['match']}")
    print(f"Overall similarity: {result['similarity']:.2f}")
    print("Differences:")
    for diff in result['differences']:
        print(f"- {diff}")