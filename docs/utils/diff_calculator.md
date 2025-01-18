Module utils.diff_calculator
============================

Functions
---------

`calculate_diff(existing, requested, key)`
:   Calculate differences between existing and requested resources.
    
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
        ...     {"name": "repo1", "visibility": "public"},
        ...     {"name": "repo2", "visibility": "private"}
        ... ]
        >>> requested = [
        ...     Repository(name="repo1", visibility="private"),
        ...     Repository(name="repo3", visibility="public")
        ... ]
        >>> to_add, to_update, to_delete = calculate_diff(existing, requested, "name")
        >>> print(to_add)
        [{'name': 'repo3', 'visibility': 'public'}]
        >>> print(to_update)
        [{'name': 'repo1', 'visibility': 'private'}]
        >>> print(to_delete)
        [{'name': 'repo2', 'visibility': 'private'}]
    
    Notes:
        - The function converts the `existing` list into a dictionary for efficient lookups.
        - The `requested` list is expected to contain Pydantic models, which are converted
          to dictionaries using their `model_dump()` method.
    
    Logs:
        - Errors encountered during the comparison process, including missing keys or attributes.