# Claude AI - refactored to so that aggregations are organized in a nested dictionary under the key metrics

def aggregate_similarity(comparison_result):
    """
    Recursively aggregate similarity scores through the nested structure of a dictionary
    produced by compare_dicts, including lists of dictionaries.

    Args:
        comparison_result (dict): The result dictionary from compare_dicts

    Returns:
        dict: The same dictionary structure with a metrics dictionary at each level
    """
    # Base case: not a dictionary
    if not isinstance(comparison_result, dict):
        # Handle case where this is a list
        if isinstance(comparison_result, list):
            return aggregate_list_similarity(comparison_result)
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
            # Recursively process nested dictionary
            result[key] = aggregate_similarity(value)

            # Extract similarity from the processed result
            if 'similarity' in result[key]:
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
            # Process the list and get its aggregated metrics
            processed_list, list_similarity, list_match = aggregate_list_similarity(value, return_metrics=True)

            # Update the list in the result
            result[key] = processed_list

            # Add list's contribution to the parent's metrics if we got valid metrics
            if list_similarity is not None:
                similarities_sum += list_similarity
                if list_match:
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


def aggregate_list_similarity(comparison_list, return_metrics=False):
    """
    Process a list to aggregate similarity metrics for its items.

    Args:
        comparison_list (list): The list to process
        return_metrics (bool): Whether to return metrics separately

    Returns:
        If return_metrics is True:
            tuple: (processed_list, similarity_score, match_boolean)
        Otherwise:
            list: The processed list
    """
    if not isinstance(comparison_list, list):
        if return_metrics:
            return comparison_list, None, None
        return comparison_list

    # Create a new list to store processed items
    processed_list = []

    # Track metrics for the list
    list_similarities_sum = 0.0
    list_match_count = 0
    list_total_items = 0

    # Process each item in the list
    for item in comparison_list:
        if isinstance(item, dict):
            # Recursively process dictionary item
            processed_item = aggregate_similarity(item)
            processed_list.append(processed_item)

            # Extract similarity from processed dictionary
            if 'similarity' in processed_item:
                list_similarities_sum += processed_item['similarity']
                if processed_item.get('match', False):
                    list_match_count += 1
                list_total_items += 1
            elif 'metrics' in processed_item:
                list_similarities_sum += processed_item['metrics']['aggregated_similarity']
                if processed_item['metrics'].get('aggregated_match', False):
                    list_match_count += 1
                list_total_items += 1
        elif isinstance(item, list):
            # Recursively process nested list
            processed_sublist, sublist_similarity, sublist_match = aggregate_list_similarity(item, return_metrics=True)
            processed_list.append(processed_sublist)

            # Add nested list's contribution to this list's metrics
            if sublist_similarity is not None:
                list_similarities_sum += sublist_similarity
                if sublist_match:
                    list_match_count += 1
                list_total_items += 1
        else:
            # Non-dict, non-list items are kept as is
            processed_list.append(item)

    # Calculate metrics for the list
    if list_total_items > 0:
        list_similarity = list_similarities_sum / list_total_items
        list_match = (list_match_count / list_total_items) >= 0.8
    else:
        list_similarity = 1.0  # Default to perfect match if list has no scorable items
        list_match = True

    # Add metrics directly to the list items if they're dictionaries
    if all(isinstance(item, dict) for item in processed_list) and processed_list:
        for item in processed_list:
            if 'metrics' not in item and 'similarity' not in item:
                item['metrics'] = {
                    'aggregated_similarity': list_similarity,
                    'aggregated_match': list_match
                }

    if return_metrics:
        return processed_list, list_similarity, list_match
    return processed_list


# Example usage
if __name__ == "__main__":
    import json
    from compare_dicts import compare_dicts

    # Sample nested dictionaries from the original code
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
    comparison_result = compare_dicts(dict3, dict4)

    # Aggregate similarity scores
    aggregated_result = aggregate_similarity(comparison_result)

    # Print results in a readable format
    print(json.dumps(aggregated_result, indent=2))