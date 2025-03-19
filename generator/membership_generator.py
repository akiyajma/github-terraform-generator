from jinja2 import Environment, FileSystemLoader


def generate_membership(membership, template_dir, output_dir, action="create"):
    """
    Generate a Terraform configuration file for GitHub membership with support for create, update, and delete actions.

    Args:
        membership (Membership): The membership object containing username.
        template_dir (str): Path to the Jinja2 template directory.
        output_dir (str): Path to the output directory.

    Returns:
        None
    """
    if action not in ["create", "update", "delete"]:
        raise ValueError(
            "Invalid action. Must be 'create', 'update', or 'delete'.")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("membership.tf.j2")

    output_path = f"{output_dir}/{membership.username}_membership.tf"

    with open(output_path, "w") as file:
        file.write(template.render(membership=membership, action=action))
