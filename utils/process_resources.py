import os

from loguru import logger

from generator.terraform_generator import TerraformGenerator
from utils.resource_changes import ResourceChanges


def process_repositories(generator, output_dir, repos_to_add, repos_to_update, repos_to_delete):
    """
    Handle the lifecycle of repositories: addition, update, and deletion.

    This function generates Terraform files for new or updated repositories and removes
    Terraform files for deleted repositories.

    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        repos_to_add (list[dict]): A list of repositories to add, represented as dictionaries.
        repos_to_update (list[dict]): A list of repositories to update, represented as dictionaries.
        repos_to_delete (list[dict]): A list of repositories to delete, represented as dictionaries.

    Raises:
        Exception: If an error occurs during any repository operation (add, update, delete).

    Example:
        process_repositories(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
            repos_to_update=[{"repository_name": "repo2", "visibility": "private"}],
            repos_to_delete=[{"repository_name": "repo3"}]
        )
    """
    try:
        # Process additions
        for repo in repos_to_add:
            try:
                generator.generate_repository(repo)
            except Exception as e:
                raise Exception(f"Error adding repository '{
                                repo.get('repository_name', 'unknown')}': {e}")

        # Process updates
        for repo in repos_to_update:
            try:
                generator.generate_repository(repo)
            except Exception as e:
                raise Exception(f"Error updating repository '{
                                repo.get('repository_name', 'unknown')}': {e}")

        # Process deletions
        for repo in repos_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{repo['repository_name']}_repository.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: {tf_file}")
            except Exception as e:
                raise Exception(f"Error deleting repository '{
                                repo.get('repository_name', 'unknown')}': {e}")
    except Exception as e:
        raise Exception(f"Unexpected error processing repositories: {e}")


def process_teams(generator, output_dir, teams_to_add, teams_to_update, teams_to_delete):
    """
    Handle the lifecycle of teams: addition, update, and deletion.

    This function generates Terraform files for new or updated teams and removes
    Terraform files for deleted teams.

    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        teams_to_add (list[dict]): A list of teams to add, represented as dictionaries.
        teams_to_update (list[dict]): A list of teams to update, represented as dictionaries.
        teams_to_delete (list[dict]): A list of teams to delete, represented as dictionaries.

    Raises:
        Exception: If an error occurs during any team operation (add, update, delete).

    Example:
        process_teams(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
            teams_to_update=[{"team_name": "team2", "privacy": "open"}],
            teams_to_delete=[{"team_name": "team3"}]
        )
    """
    try:
        # Process additions
        for team in teams_to_add:
            try:
                generator.generate_team(team)
            except Exception as e:
                raise Exception(f"Error adding team '{
                                team.get('team_name', 'unknown')}': {e}")

        # Process updates
        for team in teams_to_update:
            try:
                generator.generate_team(team)
            except Exception as e:
                raise Exception(f"Error updating team '{
                                team.get('team_name', 'unknown')}': {e}")

        # Process deletions
        for team in teams_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{team['team_name']}_team.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: {tf_file}")
            except Exception as e:
                raise Exception(f"Error deleting team '{
                                team.get('team_name', 'unknown')}': {e}")
    except Exception as e:
        raise Exception(f"Unexpected error processing teams: {e}")


def process_resources(template_dir, output_dir, resource_changes: ResourceChanges):
    """
    Orchestrate the processing of repositories and teams for addition, update, and deletion.

    This function delegates repository and team operations to the respective helper functions.

    Args:
        template_dir (str): The directory containing Jinja2 templates for Terraform files.
        output_dir (str): The directory where Terraform files will be generated or deleted.
        resource_changes (ResourceChanges): An object containing changes to repositories and teams.

    Raises:
        Exception: If an error occurs during repository or team processing.

    Example:
        resource_changes = ResourceChanges(
            repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
            repos_to_update=[{"repository_name": "repo2", "visibility": "private"}],
            repos_to_delete=[{"repository_name": "repo3"}],
            teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
            teams_to_update=[],
            teams_to_delete=[{"team_name": "team2"}]
        )
        process_resources(template_dir="templates", output_dir="output", resource_changes=resource_changes)
    """
    try:
        generator = TerraformGenerator(template_dir, output_dir)

        # Delegate repository processing
        process_repositories(
            generator,
            output_dir,
            resource_changes.repos_to_add,
            resource_changes.repos_to_update,
            resource_changes.repos_to_delete,
        )

        # Delegate team processing
        process_teams(
            generator,
            output_dir,
            resource_changes.teams_to_add,
            resource_changes.teams_to_update,
            resource_changes.teams_to_delete,
        )

        logger.info("Resource processing completed successfully.")
    except Exception as e:
        raise Exception(f"Resource processing failed: {e}")
