Module utils.diff_calculator
============================

Functions
---------

`calculate_diff(existing, requested, key)`
:   Calculate the difference between existing and requested resources (identify updates, additions, and deletions).
    
    Args:
        existing (list[dict]): A list of existing resources.
        requested (list[PydanticModel]): A list of requested new resources.
        key (str): The key to uniquely identify resources.
    
    Returns:
        tuple: A tuple containing three lists - to_update, to_add, and to_delete.