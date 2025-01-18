import os

from jinja2 import Environment, FileSystemLoader

from models import Repository


def generate_repository(repository, template_dir: str, output_dir: str):
    """
    Generate a Terraform configuration file for a GitHub repository.

    This function takes a repository object or dictionary, validates its attributes, and
    generates a Terraform configuration file using a Jinja2 template. The resulting file
    is saved to the specified output directory.

    Args:
        repository (Repository or dict): The repository data, either as a `Repository` object
            or a dictionary with the following keys:
            - `repository_name` (str): The name of the repository.
            - `description` (str, optional): A description of the repository.
            - `visibility` (str): The visibility of the repository (e.g., "public" or "private").
            - `gitignore_template` (str, optional): The Git ignore template to apply.
        template_dir (str): The directory containing the Jinja2 template files.
        output_dir (str): The directory where the generated Terraform file will be saved.

    Raises:
        ValueError: If the repository data is invalid.
        TemplateNotFound: If the Jinja2 template file is not found.
        Exception: If an error occurs during template rendering or file writing.

    Example:
        >>> repository = {
                "repository_name": "example-repo",
                "description": "An example repository",
                "visibility": "public",
                "gitignore_template": "Python"
            }
        >>> generate_repository(repository, "templates", "output")

    Notes:
        - The Jinja2 template file must be named `repository.tf.j2` and located in `template_dir`.
        - The generated file will be saved with the name `<repository_name>_repository.tf` in `output_dir`.
    """
    try:
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

    except Exception as e:
        raise Exception(f"Error generating Terraform file for repository: {e}")


def _write_to_file(output_dir: str, filename: str, content: str):
    """
    Write content to a file in the specified output directory.

    This function ensures that the output directory exists and writes the given content
    to a file with the specified name. If the directory does not exist, it is created.

    Args:
        output_dir (str): The directory where the file will be saved. If it does not exist,
            it will be created.
        filename (str): The name of the file to be created.
        content (str): The content to write to the file.

    Raises:
        OSError: If the output directory cannot be created.
        PermissionError: If the process lacks the necessary permissions to write to the file.
        Exception: For other unexpected errors during file writing.

    Example:
        >>> _write_to_file("output", "example.tf", "resource {...}")

    Notes:
        - The full path of the created file will be `<output_dir>/<filename>`.
        - The function raises an exception if writing to the file fails for any reason.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file '{filename}': {e}")
