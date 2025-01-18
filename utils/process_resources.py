import os

from generator.terraform_generator import TerraformGenerator
from utils.resource_changes import ResourceChanges


def process_repositories(generator, output_dir, repos_to_add, repos_to_update, repos_to_delete):
    """
    Process the repositories to add, update, and delete.

    Args:
        generator (TerraformGenerator): The Terraform generator instance.
        output_dir (str): The directory where the generated Terraform files will be saved.
        repos_to_add (list[Repository]): A list of repositories to add.
        repos_to_update (list[Repository]): A list of repositories to update.
        repos_to_delete (list[Repository]): A list of repositories to delete.
    """
    for repo in repos_to_add:
        generator.generate_repository(repo)
    for repo in repos_to_update:
        generator.generate_repository(repo)
    for repo in repos_to_delete:
        tf_file = os.path.join(
            output_dir, f"{repo['repository_name']}_repository.tf")
        if os.path.exists(tf_file):
            os.remove(tf_file)
            print(f"Deleted Terraform file: {tf_file}")
        else:
            print(f"Terraform file not found for deletion: {tf_file}")


def process_teams(generator, output_dir, teams_to_add, teams_to_update, teams_to_delete):
    """
    Process the teams to add, update, and delete.

    Args:
        generator (TerraformGenerator): The Terraform generator instance.
        output_dir (str): The directory where the generated Terraform files will be saved.
        teams_to_add (list[Team]): A list of teams to add.
        teams_to_update (list[Team]): A list of teams to update.
        teams_to_delete (list[Team]): A list of teams to delete.
    """
    for team in teams_to_add:
        generator.generate_team(team)
    for team in teams_to_update:
        generator.generate_team(team)
    for team in teams_to_delete:
        tf_file = os.path.join(output_dir, f"{team['team_name']}_team.tf")
        if os.path.exists(tf_file):
            os.remove(tf_file)
            print(f"Deleted Terraform file: {tf_file}")
        else:
            print(f"Terraform file not found for deletion: {tf_file}")


def process_resources(template_dir, output_dir, resource_changes: ResourceChanges):
    """
    Process the resources (repositories and teams) to add, update, and delete.

    Args:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.
        resource_changes (ResourceChanges): The changes to be applied to the resources.
    """
    generator = TerraformGenerator(template_dir, output_dir)

    process_repositories(generator, output_dir, resource_changes.repos_to_add,
                         resource_changes.repos_to_update, resource_changes.repos_to_delete)

    process_teams(generator, output_dir, resource_changes.teams_to_add,
                  resource_changes.teams_to_update, resource_changes.teams_to_delete)
