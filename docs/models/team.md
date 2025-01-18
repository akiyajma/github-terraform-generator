Module models.team
==================

Classes
-------

`Team(**data: Any)`
:   A model representing a team.
    
    Attributes:
        team_name (str): The name of the team.
        description (str): The description of the team.
        privacy (str): The privacy level of the team (closed, secret, or open).
        members (List[TeamMember]): A list of team members.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `description: str`
    :

    `members: List[models.team.TeamMember]`
    :

    `model_config`
    :

    `privacy: str`
    :

    `team_name: str`
    :

`TeamMember(**data: Any)`
:   A model representing a team member.
    
    Attributes:
        username (str): The username of the team member.
        role (str): The role of the team member (member or maintainer).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `model_config`
    :

    `role: str`
    :

    `username: str`
    :