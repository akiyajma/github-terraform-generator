def calculate_diff(existing, requested, key):
    """
    Calculate the differences between existing and requested resources.

    This function compares a list of existing resources (typically loaded from a Terraform state)
    against a list of requested resources (typically defined in configuration or input).
    It determines which resources need to be added, updated, or deleted based on a unique identifier.

    Args:
        existing (list[dict]): A list of dictionaries representing the current state of resources.
            Each dictionary **must** contain the specified `key` to uniquely identify the resource.
        requested (list[PydanticModel]): A list of Pydantic models representing the desired state
            of resources. Each model **must** include the specified `key`.
        key (str): The attribute that serves as the unique identifier for each resource.

    Returns:
        tuple: A tuple containing three lists:
            - `to_add` (list[dict]): Resources that exist in `requested` but are missing in `existing`,
              indicating they need to be added.
            - `to_update` (list[dict]): Resources that exist in both `requested` and `existing`, but
              have differences in their attributes, indicating they need to be updated.
            - `to_delete` (list[dict]): Resources that exist in `existing` but have `allow_delete=True`
              in `requested`, indicating they should be removed.

    Raises:
        KeyError: If `key` is missing in one or more dictionaries within the `existing` list.
        AttributeError: If `key` is missing in one or more models within the `requested` list.
        Exception: If an unexpected error occurs during the comparison process.

    Example:
        >>> existing = [
        ...     {"repository_name": "repo1", "visibility": "public", "description": "First repo"},
        ...     {"repository_name": "repo2", "visibility": "private", "description": "Second repo"}
        ... ]
        >>> requested = [
        ...     Repository(repository_name="repo1", visibility="private", description="Updated repo"),
        ...     Repository(repository_name="repo3", visibility="public", description="New repo")
        ... ]
        >>> to_add, to_update, to_delete = calculate_diff(existing, requested, "repository_name")
        >>> print(to_add)
        [{'repository_name': 'repo3', 'visibility': 'public', 'description': 'New repo'}]
        >>> print(to_update)
        [{'repository_name': 'repo1', 'visibility': 'private', 'description': 'Updated repo'}]
        >>> print(to_delete)
        []  # No resources marked for deletion in this example.

    Notes:
        - The function efficiently converts `existing` resources into a dictionary for **fast lookups**.
        - The `requested` list, which contains Pydantic models, is **converted to dictionaries**
          using `.model_dump()` before comparison.
        - The comparison ignores certain keys (e.g., `"allow_delete"`) to prevent unnecessary updates.
        - If a resource exists in both `existing` and `requested`, but its attributes differ,
          it will be included in `to_update`.

    Logs:
        - Logs any errors encountered, such as missing keys or attributes.
        - Logs unexpected errors with details for debugging.
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
