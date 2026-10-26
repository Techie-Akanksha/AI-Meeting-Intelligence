def clean_text_items(items):
    return [
        item.strip()
        for item in items
        if isinstance(item, str)
        and item.strip()
        and item.strip().lower() != "not specified"
    ]

def validate_meeting_data(data):
    """Validate and normalize the LLM meeting response."""

    if not isinstance(data, dict):
        raise ValueError("Meeting response must be a JSON object.")

    if not isinstance(data.get("summary"), str):
        raise ValueError("Summary must be a string.")

    text_fields = [
        "discussion_points",
        "decisions",
        "open_questions"
    ]

    for field in text_fields:
        items = data.get(field)

        if not isinstance(items, list):
            raise ValueError(f"{field} must be a list.")

        if not all(isinstance(item, str) for item in items):
            raise ValueError(f"{field} must contain only strings.")

        data[field] = clean_text_items(items)

    object_fields = {
        "action_items": ["task", "person", "deadline"],
        "additional_insights": [
            "category", "details", "status", "evidence"
        ]
    }

    for field, required_keys in object_fields.items():
        items = data.get(field)

        if not isinstance(items, list):
            raise ValueError(f"{field} must be a list.")

        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"{field} must contain objects.")

            for key in required_keys:
                if not isinstance(item.get(key), str):
                    raise ValueError(
                        f"{field}: '{key}' must be a string."
                    )

    return data
