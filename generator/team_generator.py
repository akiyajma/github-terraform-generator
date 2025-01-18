import os

from jinja2 import Environment, FileSystemLoader

from models import Team


def generate_team(team: Team, template_dir: str, output_dir: str):
    """
    Generate a Terraform configuration file for a GitHub team.

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
    """

    try:
        if isinstance(team, dict):
            team = Team(**team)

        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("team.tf.j2")

        rendered_code = template.render(
            team_name=team.team_name,
            description=team.description,
            privacy=team.privacy,
            members=team.members
        )

        _write_to_file(output_dir, f"{team.team_name}_team.tf", rendered_code)

    except Exception as e:
        raise Exception(f"Error generating Terraform file for team: {e}")


def _write_to_file(output_dir: str, filename: str, content: str):
    """
    Write content to a file in the specified output directory.

    This function ensures that the output directory exists, creates it if necessary,
    and writes the given content to a file with the specified name.

    Args:
        output_dir (str): The path to the directory where the file will be saved.
            If the directory does not exist, it will be created.
        filename (str): The name of the file to be created.
        content (str): The content to be written to the file.

    Raises:
        OSError: If the output directory cannot be created or accessed.
        PermissionError: If there are insufficient permissions to write to the file.
        Exception: For any other errors encountered during file writing.

    Example:
        >>> _write_to_file("output", "team_config.tf", "resource {...}")

    Notes:
        - The file path will be constructed as `<output_dir>/<filename>`.
        - Any exceptions encountered will provide detailed error messages.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file '{filename}': {e}")
