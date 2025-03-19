import os

from jinja2 import Environment, FileSystemLoader


def generate_membership(membership, template_dir: str, output_dir: str, action="create"):
    """
    Generate a Terraform configuration file for GitHub membership management.

    This function creates, updates, or deletes a Terraform configuration file for a GitHub
    membership using a Jinja2 template. The membership configuration includes the username
    and role, and the generated file is saved in the specified output directory.

    Args:
        membership (Membership): A membership object containing:
            - `username` (str): The GitHub username of the member.
            - `role` (str): The role assigned to the user ("member" or "admin").
        template_dir (str): The directory containing Jinja2 template files.
        output_dir (str): The directory where the generated Terraform file will be saved.
        action (str, optional): Specifies the operation to be performed. Must be one of:
            - `"create"`: Generates a new membership configuration.
            - `"update"`: Updates an existing membership configuration.
            - `"delete"`: Removes the membership configuration.
            Defaults to `"create"`.

    Raises:
        ValueError: If the `action` argument is not one of `"create"`, `"update"`, or `"delete"`.
        TemplateNotFound: If the required Jinja2 template file (`membership.tf.j2`) is missing.
        Exception: If an error occurs during template rendering or file writing.

    Example:
        >>> from models.membership import Membership
        >>> membership = Membership(username="user1", role="member")
        >>> generate_membership(membership, "templates", "output")

    Notes:
        - The Jinja2 template file must be named `membership.tf.j2` and located in `template_dir`.
        - The generated file will be saved as `<username>_membership.tf` in `output_dir`.
        - The `action` parameter determines whether the configuration is for creation, update, or deletion.
    """
    if action not in ["create", "update", "delete"]:
        raise ValueError(
            "Invalid action. Must be 'create', 'update', or 'delete'.")

    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("membership.tf.j2")

        rendered_code = template.render(membership=membership, action=action)

        _write_to_file(
            output_dir, f"{membership.username}_membership.tf", rendered_code)

    except Exception as e:
        raise Exception(
            f"Error generating Terraform file for membership '{membership.username}': {e}")


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
        - It ensures that the output directory is created if it does not already exist.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file '{filename}': {e}")
