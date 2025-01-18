Module generator.team_generator
===============================

Functions
---------

`generate_team(team: models.team.Team, template_dir: str, output_dir: str)`
:   Generate a Terraform configuration file for a GitHub team.
    
    This function takes a `Team` object or a dictionary with team attributes, validates
    the input, and generates a Terraform configuration file by rendering a Jinja2 template.
    The output file is saved in the specified directory.
    
    Args:
        team (Team or dict): A `Team` object or dictionary with the following attributes:
            - `team_name` (str): The name of the team.
            - `description` (str, optional): A description of the team.
            - `privacy` (str): The privacy level of the team (e.g., "closed", "secret").
            - `members` (list[dict], optional): A list of team members, where each member
              is represented as a dictionary with `username` and `role` keys.
        template_dir (str): The directory containing the Jinja2 template files.
        output_dir (str): The directory where the Terraform configuration file will be saved.
    
    Raises:
        ValueError: If the `team` object is invalid or lacks required attributes.
        FileNotFoundError: If the specified template file is not found in `template_dir`.
        Exception: If any error occurs during rendering or file writing.
    
    Example:
        >>> team = Team(
                team_name="dev-team",
                description="Development team",
                privacy="closed",
                members=[{"username": "dev1", "role": "maintainer"}]
            )
        >>> generate_team(team, "templates", "output")
    
    Notes:
        - The Jinja2 template file should be named `team.tf.j2` and located in `template_dir`.
        - The output file will be saved as `<team_name>_team.tf` in the specified `output_dir`.
        - If a dictionary is passed instead of a `Team` object, it will be converted internally.