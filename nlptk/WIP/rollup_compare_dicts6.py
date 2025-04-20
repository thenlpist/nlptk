# Claude AI
def aggregate_similarity(comparison_result):
    """
    Recursively aggregate similarity scores through the nested structure of a dictionary
    produced by compare_dicts, including lists of dictionaries.
    Ignores empty leaf nodes (where is_empty=True) when calculating aggregated scores.

    Args:
        comparison_result (dict): The result dictionary from compare_dicts

    Returns:
        dict: The same dictionary structure with a metrics dictionary at each level
    """
    # Base case: not a dictionary
    if not isinstance(comparison_result, dict):
        # Handle case where this is a list
        if isinstance(comparison_result, list):
            return process_list(comparison_result)
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

    # Clean up any old metrics if present
    if 'metrics' in result:
        del result['metrics']

    # Process all keys except our metrics key
    keys_to_process = [k for k in result.keys() if k != 'metrics']

    for key in keys_to_process:
        value = result[key]

        if isinstance(value, dict):
            # Skip empty leaf nodes
            if 'is_empty' in value and value['is_empty'] == True:
                continue

            # Recursively process nested dictionary
            result[key] = aggregate_similarity(value)

            # Extract similarity from the processed result
            if 'similarity' in result[key]:
                # Skip empty nodes when aggregating
                if 'is_empty' in result[key] and result[key]['is_empty'] == True:
                    continue

                similarities_sum += result[key]['similarity']
                if result[key].get('match', False):
                    match_count += 1
                total_items += 1
            elif 'metrics' in result[key]:
                similarities_sum += result[key]['metrics']['aggregated_similarity']
                if result[key]['metrics'].get('aggregated_match', False):
                    match_count += 1
                total_items += 1

        elif isinstance(value, list):
            # Convert the list to a structured format with items and metrics
            result[key] = process_list(value)

            # Extract metrics from the processed list
            if 'metrics' in result[key]:
                similarities_sum += result[key]['metrics']['aggregated_similarity']
                if result[key]['metrics'].get('aggregated_match', False):
                    match_count += 1
                total_items += 1

    # Calculate aggregated metrics for this level
    if total_items > 0:
        result['metrics'] = {
            'aggregated_similarity': round(similarities_sum / total_items, 4),
            'aggregated_match': (match_count / total_items) >= 0.8
        }
    else:
        # Edge case: no scorable items at this level
        result['metrics'] = {
            'aggregated_similarity': 1.0,  # Default to perfect match if no items to compare
            'aggregated_match': True
        }

    return result


def process_list(comparison_list):
    """
    Process a list and convert it to a structured format with items and metrics.
    Ignores empty leaf nodes (where is_empty=True) when calculating aggregated scores.

    Args:
        comparison_list (list): The list to process

    Returns:
        dict: A dictionary with 'items' containing the processed list and 'metrics'
    """
    # Handle non-list inputs
    if not isinstance(comparison_list, list):
        return comparison_list

    # Create structure for processed list
    result = {
        'items': [],
        'metrics': {
            'aggregated_similarity': 0.0,
            'aggregated_match': False
        }
    }

    # Track metrics for the list
    similarities_sum = 0.0
    match_count = 0
    total_items = 0

    # Process each item in the list
    for item in comparison_list:
        if isinstance(item, dict):
            # Skip empty leaf nodes
            if 'is_empty' in item and item['is_empty'] == True:
                result['items'].append(item)  # Still include it in the items list
                continue

            # Recursively process dictionary item
            processed_item = aggregate_similarity(item)
            result['items'].append(processed_item)

            # Extract similarity from processed dictionary
            if 'similarity' in processed_item:
                # Skip empty nodes when aggregating
                if 'is_empty' in processed_item and processed_item['is_empty'] == True:
                    continue

                similarities_sum += processed_item['similarity']
                if processed_item.get('match', False):
                    match_count += 1
                total_items += 1
            elif 'metrics' in processed_item:
                similarities_sum += processed_item['metrics']['aggregated_similarity']
                if processed_item['metrics'].get('aggregated_match', False):
                    match_count += 1
                total_items += 1
        elif isinstance(item, list):
            # Process nested list
            processed_sublist = process_list(item)
            result['items'].append(processed_sublist)

            # Extract metrics from nested list
            if 'metrics' in processed_sublist:
                similarities_sum += processed_sublist['metrics']['aggregated_similarity']
                if processed_sublist['metrics'].get('aggregated_match', False):
                    match_count += 1
                total_items += 1
        else:
            # Non-dict, non-list items are kept as is
            result['items'].append(item)
            # These items don't contribute to similarity calculations

    # Calculate metrics for the list
    if total_items > 0:
        result['metrics'] = {
            'aggregated_similarity': round(similarities_sum / total_items, 4),
            'aggregated_match': (match_count / total_items) >= 0.8
        }
    else:
        # Edge case: no scorable items
        result['metrics'] = {
            'aggregated_similarity': 1.0,  # Default to perfect match if list has no scorable items
            'aggregated_match': True
        }

    return result


# Example usage
if __name__ == "__main__":
    import json
    from compare_dicts import compare_dicts

    # Sample nested dictionaries with some empty values
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
                "nickname": "",  # Empty string
                "summary": "Supported senior sales team members in prospecting new clients and maintaining existing accounts.",
                "highlights": ["Achieved 100 of personal sales targets."]
            }
        ]
    }

    # Compare dictionaries
    comparison_result = compare_dicts(dict3, dict4)

    # Aggregate similarity scores
    aggregated_result = aggregate_similarity(comparison_result)

    # Print results in a readable format
    print(json.dumps(aggregated_result, indent=2))