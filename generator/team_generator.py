import os

from jinja2 import Environment, FileSystemLoader

from models import Team


def generate_team(team: Team, template_dir: str, output_dir: str):
    """
    Generate a Terraform file for a GitHub team.

    Args:
        team (Team): The team object containing team attributes.
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform file will be saved.
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("team.tf.j2")

    rendered_code = template.render(
        team_name=team.team_name,
        description=team.description,
        privacy=team.privacy,
        members=team.members
    )

    _write_to_file(output_dir, f"{team.team_name}_team.tf", rendered_code)


def _write_to_file(output_dir: str, filename: str, content: str):
    """
    Write the rendered content to a file.

    Args:
        output_dir (str): The directory where the file will be saved.
        filename (str): The name of the file to be created.
        content (str): The content to be written to the file.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Generated Terraform file: {file_path}")
