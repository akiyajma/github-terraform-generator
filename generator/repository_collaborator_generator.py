from jinja2 import Environment, FileSystemLoader


def generate_repository_collaborator(repository_collaborator, template_dir, output_dir, action="create"):
    if action not in ["create", "update", "delete"]:
        raise ValueError(
            "Invalid action. Must be 'create', 'update', or 'delete'.")

    print(repository_collaborator)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("repository_collaborator.tf.j2")

    output_path = f"{output_dir}/{repository_collaborator.username}_{repository_collaborator.repository_name}_collaborator.tf"
    with open(output_path, "w") as file:
        file.write(template.render(
            repository_collaborator=repository_collaborator, action=action))
