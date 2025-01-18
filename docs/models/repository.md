Module models.repository
========================

Classes
-------

`Repository(**data: Any)`
:   A model representing a repository.
    
    Attributes:
        repository_name (str): The name of the repository.
        description (str): The description of the repository.
        visibility (str): The visibility of the repository (public, private, or internal).
        gitignore_template (str): The gitignore template to use for the repository.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `description: str`
    :

    `gitignore_template: str`
    :

    `model_config`
    :

    `repository_name: str`
    :

    `visibility: str`
    :