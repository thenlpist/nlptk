# Claude AI - correct code, but doesn't handle lists of dict

def aggregate_similarity(comparison_result):
    """
    Recursively aggregate similarity scores through the nested structure of a dictionary
    produced by compare_dicts.

    Args:
        comparison_result (dict): The result dictionary from compare_dicts

    Returns:
        dict: The same dictionary structure with aggregated similarity scores at each level
    """
    # Base case: not a dictionary
    if not isinstance(comparison_result, dict):
        return comparison_result

    # Create a copy of the result to avoid modifying the original
    result = comparison_result.copy()

    # Check if this is a leaf comparison result (contains 'similarity' key)
    if 'similarity' in result:
        # This is a leaf node, return as is
        return result

    # Special case for status dictionaries
    if 'status' in result:
        if result['status'] in ['missing_in_dict1', 'missing_in_dict2', 'type_mismatch']:
            # Missing keys or type mismatches have zero similarity
            result['similarity'] = 0.0
            result['match'] = False
            return result
        elif result['status'] == 'unsupported_type' and 'match' in result:
            # Use existing match information
            result['similarity'] = 1.0 if result['match'] else 0.0
            return result

    # Initialize counters for similarity calculation
    similarities_sum = 0.0
    match_count = 0
    total_items = 0

    # Process all keys except our own aggregation keys
    keys_to_process = [k for k in result.keys() if k not in ['aggregated_similarity', 'aggregated_match']]

    for key in keys_to_process:
        value = result[key]

        if isinstance(value, dict):
            # Recursively process nested dictionary
            result[key] = aggregate_similarity(value)

            # Extract similarity from the processed result
            if 'similarity' in result[key]:
                similarities_sum += result[key]['similarity']
                if result[key].get('match', False):
                    match_count += 1
                total_items += 1
            elif 'aggregated_similarity' in result[key]:
                similarities_sum += result[key]['aggregated_similarity']
                if result[key].get('aggregated_match', False):
                    match_count += 1
                total_items += 1

        elif isinstance(value, list):
            list_similarities_sum = 0.0
            list_match_count = 0
            list_total_items = 0

            # Create a new list to store processed items
            new_list = []

            for item in value:
                if isinstance(item, dict):
                    processed_item = aggregate_similarity(item)
                    new_list.append(processed_item)

                    # Extract similarity from processed list item
                    if 'similarity' in processed_item:
                        list_similarities_sum += processed_item['similarity']
                        if processed_item.get('match', False):
                            list_match_count += 1
                        list_total_items += 1
                    elif 'aggregated_similarity' in processed_item:
                        list_similarities_sum += processed_item['aggregated_similarity']
                        if processed_item.get('aggregated_match', False):
                            list_match_count += 1
                        list_total_items += 1
                else:
                    # Non-dictionary items are kept as is
                    new_list.append(item)

            # Update the list in the result
            result[key] = new_list

            # Calculate aggregated metrics for the list
            if list_total_items > 0:
                list_similarity = list_similarities_sum / list_total_items
                list_match = (list_match_count / list_total_items) >= 0.8

                # Add list's contribution to the parent's metrics
                similarities_sum += list_similarity
                if list_match:
                    match_count += 1
                total_items += 1

    # Calculate aggregated metrics for this level
    if total_items > 0:
        result['aggregated_similarity'] = round(similarities_sum / total_items, 4)
        result['aggregated_match'] = (match_count / total_items) >= 0.8
    else:
        # Edge case: no scorable items at this level
        result['aggregated_similarity'] = 1.0  # Default to perfect match if no items to compare
        result['aggregated_match'] = True

    return result


# Example usage
if __name__ == "__main__":
    import json
    from compare_dicts import compare_dicts

    # Sample nested dictionaries
    dict1 = {
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

    dict2 = {
        "personal": {
            "name": "Jon Smith",  # Slightly different
            "email": "john.smith@example.com"
        },
        "address": {
            "street": "123 Main St",  # Abbreviated
            "city": "New York",
            "zip": "10001"
        }
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
                "nickname": "",
                "summary": "Supported senior sales team members in prospecting new clients and maintaining existing accounts.",
                "highlights": ["Achieved 100% of personal sales targets.",
                               "Assisted in preparing sales presentations."]
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
                "nickname": "",
                "summary": "Supported senior sales team members in prospecting new clients and maintaining existing accounts.",
                "highlights": ["Achieved 100 of personal sales targets."]
            }
        ]
    }

    # Compare dictionaries
    comparison_result = compare_dicts(dict3, dict4, threshold=0.8)

    # Aggregate similarity scores
    aggregated_result = aggregate_similarity(comparison_result)

    # Print results in a readable format
    print(json.dumps(aggregated_result, indent=2))

