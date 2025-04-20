# another from Claude
def compare_dicts(dict1, dict2, threshold=0.8):
    """
    Recursively compare two nested dictionaries where leaf values are strings.
    Handles nested lists of dictionaries as well.
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
            'similarity': float,  # Overall similarity score (0.0-1.0)
            'leaf_results': dict  # Results for each leaf node
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
        leaf_results = {}

        # Handle case when both are dictionaries
        if isinstance(d1, dict) and isinstance(d2, dict):
            # Check for keys in d1
            for key in d1:
                total_items += 1
                current_path = path + [key]
                path_str = '.'.join(str(p) for p in current_path)

                if key not in d2:
                    differences.append(f"Key '{path_str}' missing in second dictionary")
                    leaf_results[path_str] = {
                        'status': 'missing_in_second',
                        'value1': d1[key],
                        'value2': None,
                        'similarity': 0.0
                    }
                    continue

                # Recurse into nested structures
                sub_result = compare_recursive(d1[key], d2[key], current_path)
                differences.extend(sub_result['differences'])
                total_similarity += sub_result['similarity'] * sub_result['item_count']
                total_items += sub_result['item_count'] - 1  # -1 because we already counted this key
                leaf_results.update(sub_result['leaf_results'])

            # Check for keys in d2 not in d1
            for key in d2:
                if key not in d1:
                    current_path = path + [key]
                    path_str = '.'.join(str(p) for p in current_path)
                    differences.append(f"Key '{path_str}' missing in first dictionary")
                    leaf_results[path_str] = {
                        'status': 'missing_in_first',
                        'value1': None,
                        'value2': d2[key],
                        'similarity': 0.0
                    }
                    total_items += 1

        # Handle case when both are lists
        elif isinstance(d1, list) and isinstance(d2, list):
            # For lists, compare items at each index when possible
            max_len = max(len(d1), len(d2))

            if max_len == 0:
                # Both lists empty
                return {
                    'differences': [],
                    'similarity': 1.0,
                    'item_count': 1,
                    'leaf_results': {}
                }

            list_similarity = 0.0

            # Compare items that exist in both lists
            for i in range(min(len(d1), len(d2))):
                current_path = path + [i]
                sub_result = compare_recursive(d1[i], d2[i], current_path)
                differences.extend(sub_result['differences'])
                list_similarity += sub_result['similarity'] * sub_result['item_count']
                total_items += sub_result['item_count']
                leaf_results.update(sub_result['leaf_results'])

            # Handle unmatched items in first list
            for i in range(len(d2), len(d1)):
                current_path = path + [i]
                path_str = '.'.join(str(p) for p in current_path)
                differences.append(f"Item at index {i} in '{path_str[:-2]}' missing in second list")

                # If it's a leaf node
                if isinstance(d1[i], str):
                    leaf_results[path_str] = {
                        'status': 'missing_in_second',
                        'value1': d1[i],
                        'value2': None,
                        'similarity': 0.0
                    }
                total_items += 1

            # Handle unmatched items in second list
            for i in range(len(d1), len(d2)):
                current_path = path + [i]
                path_str = '.'.join(str(p) for p in current_path)
                differences.append(f"Item at index {i} in '{path_str[:-2]}' missing in first list")

                # If it's a leaf node
                if isinstance(d2[i], str):
                    leaf_results[path_str] = {
                        'status': 'missing_in_first',
                        'value1': None,
                        'value2': d2[i],
                        'similarity': 0.0
                    }
                total_items += 1

            # Calculate overall list similarity
            total_similarity = list_similarity if total_items == 0 else list_similarity

        # Handle case when both are strings (leaf nodes)
        elif isinstance(d1, str) and isinstance(d2, str):
            similarity = calculate_similarity(d1, d2)
            total_similarity = similarity
            total_items = 1
            path_str = '.'.join(str(p) for p in path)

            status = 'match' if similarity >= threshold else 'different'
            leaf_results[path_str] = {
                'status': status,
                'value1': d1,
                'value2': d2,
                'similarity': similarity
            }

            if similarity < threshold:
                differences.append(
                    f"String values differ at '{path_str}': "
                    f"'{d1}' vs '{d2}' (similarity: {similarity:.2f})"
                )

        # Handle type mismatches
        else:
            path_str = '.'.join(str(p) for p in path)
            differences.append(
                f"Type mismatch at '{path_str}': "
                f"{type(d1).__name__} vs {type(d2).__name__}"
            )

            leaf_results[path_str] = {
                'status': 'type_mismatch',
                'value1': str(d1) if not isinstance(d1, (dict, list)) else type(d1).__name__,
                'value2': str(d2) if not isinstance(d2, (dict, list)) else type(d2).__name__,
                'similarity': 0.0
            }

            total_similarity = 0
            total_items = 1

        # Calculate average similarity for this level
        avg_similarity = total_similarity / total_items if total_items > 0 else 0.0

        return {
            'differences': differences,
            'similarity': avg_similarity,
            'item_count': total_items,
            'leaf_results': leaf_results
        }

    # Perform the comparison
    result = compare_recursive(dict1, dict2)

    # Return final output
    return {
        'match': len(result['differences']) == 0,
        'differences': result['differences'],
        'similarity': result['similarity'],
        'leaf_results': result['leaf_results']
    }


# Example usage
if __name__ == "__main__":
    dict1 = {
        "person": {
            "name": "John Smith",
            "address": {
                "street": "123 Main St",
                "city": "New York"
            },
            "phones": [
                {"type": "home", "number": "555-1234"},
                {"type": "work", "number": "555-5678"}
            ]
        },
        "contacts": ["john@example.com", "jsmith@work.com"]
    }

    dict2 = {
        "person": {
            "name": "Jon Smyth",
            "address": {
                "street": "123 Main Street",
                "city": "New York"
            },
            "phones": [
                {"type": "home", "number": "555-1234"},
                {"type": "mobile", "number": "555-9876"}
            ]
        },
        "contacts": ["john@example.com"],
        "extra": "something"
    }

    result = compare_dicts(dict1, dict2)
    print(f"Match: {result['match']}")
    print(f"Overall similarity: {result['similarity']:.2f}")

    print("\nDifferences:")
    for diff in result['differences']:
        print(f"- {diff}")

    print("\nLeaf node results:")
    for path, node_result in result['leaf_results'].items():
        print(f"\n{path}:")
        print(f"  Status: {node_result['status']}")
        print(f"  Value1: {node_result['value1']}")
        print(f"  Value2: {node_result['value2']}")
        print(f"  Similarity: {node_result['similarity']:.2f}")