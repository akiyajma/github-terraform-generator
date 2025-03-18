def calculate_diff(existing, requested, key):
    """
    Calculate differences between existing and requested resources.

    This function compares the existing and requested resource lists, identifying
    resources to add, update, or delete based on a unique key.

    Args:
        existing (list[dict]): A list of dictionaries representing existing resources.
            Each dictionary must include the specified `key` to uniquely identify the resource.
        requested (list[PydanticModel]): A list of Pydantic models representing the desired state
            of resources. Each model must include the specified `key`.
        key (str): The key used to uniquely identify resources in both lists.

    Returns:
        tuple: A tuple of three lists:
            - `to_add` (list): Resources in `requested` but not in `existing`.
            - `to_update` (list): Resources in `requested` with the same key but differing values in `existing`.
            - `to_delete` (list): Resources in `existing` but not in `requested`.

    Raises:
        KeyError: If `key` is missing in the `existing` resources.
        AttributeError: If `key` is missing in the `requested` resources.
        Exception: For other unexpected errors during the comparison process.

    Example:
        >>> existing = [
        ...     {"name": "repo1", "visibility": "public", "description": "First repo", "gitignore_template": "Python"},
        ...     {"name": "repo2", "visibility": "private", "description": "Second repo", "gitignore_template": "None"}
        ... ]
        >>> requested = [
        ...     Repository(name="repo1", visibility="private", description="Updated repo", gitignore_template="Go"),
        ...     Repository(name="repo3", visibility="public", description="New repo", gitignore_template="Java")
        ... ]
        >>> to_add, to_update, to_delete = calculate_diff(existing, requested, "name")
        >>> print(to_add)
        [{'name': 'repo3', 'visibility': 'public', 'description': 'New repo', 'gitignore_template': 'Java'}]
        >>> print(to_update)
        [{'name': 'repo1', 'visibility': 'private', 'description': 'Updated repo', 'gitignore_template': 'Go'}]
        >>> print(to_delete)
        [{'name': 'repo2', 'visibility': 'private', 'description': 'Second repo', 'gitignore_template': 'None'}]

    Notes:
        - The function converts the `existing` list into a dictionary for efficient lookups.
        - The `requested` list is expected to contain Pydantic models, which are converted
          to dictionaries using their `model_dump()` method.

    Logs:
        - Errors encountered during the comparison process, including missing keys or attributes.
    """
    try:
        # Convert lists to dictionaries using the unique key
        existing_dict = {item[key]: item for item in existing}
        requested_dict = {getattr(item, key): item.model_dump()
                          for item in requested}

        def normalize_dict(resource):
            # Remove keys that should not affect comparison
            ignored_keys = {"allow_delete"}
            return {k: v for k, v in resource.items() if k not in ignored_keys}

        # Determine additions
        to_add = [requested_dict[name]
                  for name in requested_dict if name not in existing_dict]

        # Determine updates
        to_update = [
            requested_dict[name]
            for name in requested_dict
            if name in existing_dict and normalize_dict(existing_dict[name]) != normalize_dict(requested_dict[name])
        ]

        # Determine deletions
        to_delete = [
            existing_dict[name]
            for name in existing_dict
            if name in requested_dict and requested_dict[name].get("allow_delete", False)
        ]

        return to_add, to_update, to_delete
    except KeyError as e:
        raise KeyError(f"Missing required key '{
                       key}' in existing resources: {e}")
    except AttributeError as e:
        raise AttributeError(f"Missing required attribute '{
                             key}' in requested resources: {e}")
    except Exception as e:
        raise Exception(f"Error calculating resource differences: {e}")
