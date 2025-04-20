# Claude AI - Doesn't work correctly

def aggregate_similarity(comparison_result):
    """
    Recursively aggregate similarity scores through the nested structure of a dictionary
    produced by compare_dicts.

    Args:
        comparison_result (dict): The result dictionary from compare_dicts

    Returns:
        dict: The same dictionary structure with aggregated similarity scores at each level
    """
    if not isinstance(comparison_result, dict):
        return comparison_result

    # Initialize variables to track similarity metrics
    total_similarity = 0.0
    total_weight = 0.0
    total_items = 0
    matches = 0

    # Create a copy of the result to avoid modifying the original
    result = comparison_result.copy()

    # Check if this is a leaf comparison result (contains 'similarity' key)
    if 'similarity' in result:
        # It's already a leaf node with similarity score, just return it
        return result

    # Process child keys
    for key, value in list(result.items()):
        if isinstance(value, dict):
            # Status keys like 'missing_in_dict1' don't need recursion
            if 'status' in value and value['status'] in ['missing_in_dict1', 'missing_in_dict2', 'type_mismatch',
                                                         'unsupported_type']:
                # These are special case dictionaries, treat according to status
                if value['status'] in ['missing_in_dict1', 'missing_in_dict2']:
                    # Missing keys should have zero similarity
                    value['similarity'] = 0.0
                    value['match'] = False
                    total_items += 1
                elif value['status'] == 'type_mismatch':
                    # Type mismatches have zero similarity
                    value['similarity'] = 0.0
                    value['match'] = False
                    total_items += 1
                elif value['status'] == 'unsupported_type' and 'match' in value:
                    # If we have a match field, use it
                    value['similarity'] = 1.0 if value['match'] else 0.0
                    total_items += 1
                    if value['match']:
                        matches += 1
                        total_similarity += 1.0
                    total_weight += 1.0
            else:
                # Recursively aggregate similarity for nested dict
                result[key] = aggregate_similarity(value)
                # Extract aggregated similarity from nested level
                if 'aggregated_similarity' in result[key]:
                    similarity = result[key]['aggregated_similarity']
                    total_similarity += similarity
                    total_weight += 1.0
                    total_items += 1
                    if result[key].get('aggregated_match', False):
                        matches += 1
        elif isinstance(value, list):
            # Handle lists by recursively aggregating each item
            new_list = []
            list_similarity = 0.0
            list_matches = 0

            for i, item in enumerate(value):
                if isinstance(item, (dict, list)):
                    processed_item = aggregate_similarity(item)
                    new_list.append(processed_item)
                    if isinstance(processed_item, dict) and 'aggregated_similarity' in processed_item:
                        list_similarity += processed_item['aggregated_similarity']
                        if processed_item.get('aggregated_match', False):
                            list_matches += 1
                else:
                    new_list.append(item)

            # Calculate list's aggregated similarity if there are items
            if len(value) > 0:
                list_agg_similarity = list_similarity / len(value)
                list_agg_match = list_matches / len(value) >= 0.8  # Using 0.8 as default threshold

                # Attach aggregated metrics to list
                result[key] = new_list
                total_similarity += list_agg_similarity
                total_weight += 1.0
                total_items += 1
                if list_agg_match:
                    matches += 1

    # Calculate aggregated similarity for current level
    if total_weight > 0:
        aggregated_similarity = total_similarity / total_weight
        # Determine if this level is a match overall (using threshold of 0.8)
        aggregated_match = matches / total_items >= 0.8 if total_items > 0 else False

        # Add aggregated metrics to result dictionary
        result['aggregated_similarity'] = round(aggregated_similarity, 4)
        result['aggregated_match'] = aggregated_match
    else:
        # No weighted items found, set defaults
        result['aggregated_similarity'] = 0.0
        result['aggregated_match'] = False

    return result


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