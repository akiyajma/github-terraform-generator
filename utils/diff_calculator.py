def calculate_diff(existing, requested, key):
    """
    Calculate the difference between existing and requested resources (identify updates, additions, and deletions).

    Args:
        existing (list[dict]): A list of existing resources.
        requested (list[PydanticModel]): A list of requested new resources.
        key (str): The key to uniquely identify resources.

    Returns:
        tuple: A tuple containing three lists - to_update, to_add, and to_delete.
    """
    existing_dict = {item[key]: item for item in existing}
    requested_dict = {getattr(item, key): item.model_dump()
                      for item in requested}

    to_update = []
    for name in requested_dict:
        if name in existing_dict and existing_dict[name] != requested_dict[name]:
            to_update.append(requested_dict[name])

    to_add = []
    for name in requested_dict:
        if name not in existing_dict:
            to_add.append(requested_dict[name])

    to_delete = []
    for name in existing_dict:
        if name not in requested_dict:
            to_delete.append(existing_dict[name])

    return to_add, to_update, to_delete
