import os

from jinja2 import Environment, FileSystemLoader

from models import Repository


def generate_repository(repository, template_dir: str, output_dir: str):
    """
    Generate a Terraform file for a GitHub repository.

    Args:
        repository (Repository or dict): The repository object or dictionary containing repository attributes.
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform file will be saved.

    Raises:
        ValidationError: If the repository data is invalid.
    """
    if isinstance(repository, dict):
        repository = Repository(**repository)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("repository.tf.j2")

    rendered_code = template.render(
        repository_name=repository.repository_name,
        description=repository.description,
        visibility=repository.visibility,
        gitignore_template=repository.gitignore_template
    )

    _write_to_file(
        output_dir, f"{repository.repository_name}_repository.tf", rendered_code)


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
