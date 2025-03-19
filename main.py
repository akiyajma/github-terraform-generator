import json
import os
import sys

from loguru import logger

from config.config_loader import load_config
from logging_config import setup_logging
from models.membership import Membership
from models.repository import Repository
from models.team import Team
from utils.diff_calculator import calculate_diff
from utils.process_resources import process_resources
from utils.resource_changes import ResourceChanges
from utils.tfstate_loader import extract_resources, load_tfstate, save_existing_state

# Set up logging using loguru
setup_logging()


def main(output_dir_override=None):
    """
    Main function to manage and apply changes to the Terraform state.

    This function is responsible for processing GitHub repositories, teams, memberships,
    and repository collaborators, comparing them with the existing Terraform state, and applying
    necessary changes through Terraform configuration files.

    The process includes:
    1. Loading the application configuration from `config.yaml`.
    2. Loading the existing Terraform state from the specified `.tfstate` file.
    3. Extracting relevant resources (repositories, teams, memberships, and collaborators) from Terraform state.
    4. Fetching new resource definitions from environment variables.
    5. Applying default values for missing attributes using `config.yaml`.
    6. Calculating the differences (additions, updates, deletions) between existing and new resources.
    7. Generating, updating, or deleting Terraform configuration files based on the computed differences.

    Args:
        output_dir_override (str, optional): A custom output directory. If not provided,
            the directory specified in `config.yaml` is used.

    Environment Variables:
        - `REPOSITORIES` (str): JSON array defining repositories.
            Each repository should have:
            - `repository_name` (str, required): The repository's name.
            - `description` (str, optional): A description of the repository.
            - `visibility` (str, required): "public", "private", or "internal".
            - `gitignore_template` (str, optional): A predefined `.gitignore` template.
              If set to `"None"`, it is omitted.

        - `TEAMS` (str): JSON array defining teams.
            Each team should have:
            - `team_name` (str, required): The team’s name.
            - `description` (str, optional): A short description.
            - `privacy` (str, required): "closed" or "secret".
            - `members` (list[dict], optional): A list of members, each having:
                - `username` (str, required): The GitHub username.
                - `role` (str, required): "maintainer" or "member".

        - `MEMBERSHIPS` (str): JSON array defining user memberships.
            Each membership should have:
            - `username` (str, required): The GitHub username.
            - `role` (str, required): "admin" or "member".

        - `REPOSITORY_COLLABORATORS` (str): JSON array defining repository collaborators.
            Each collaborator should have:
            - `repository_name` (str, required): The repository name.
            - `username` (str, required): The collaborator's GitHub username.
            - `permission` (str, required): "pull", "push", or "admin".

    Configuration:
        - The `config.yaml` file defines default values for missing attributes.
        - The Terraform state file (`terraform.tfstate`) is used to track existing resources.

    Raises:
        - `SystemExit`: If any unhandled error occurs, the script exits with status code 1.

    Logs:
        - Logs the processing steps, including resource comparisons and updates.
        - Logs errors when operations fail.

    Example Usage:
        To override the output directory and apply changes:
        >>> main(output_dir_override="/custom/output/dir")

    File References:
        - Configuration file: `config/config.yaml`
        - Terraform state file: `<output_dir>/terraform.tfstate`
        - Saved resource state: `<output_dir>/existing_resources.json`

    Notes:
        - If a `gitignore_template` is set to `"None"`, it is excluded from the Terraform configuration.
        - The script ensures only necessary changes are applied, minimizing updates to existing resources.
    """
    try:
        # Load configuration
        config = load_config()
        output_dir = output_dir_override or config["output_dir"]

        # Define file paths
        tfstate_file = os.path.join(output_dir, config["tfstate_file"])
        state_file = os.path.join(output_dir, config["state_file"])

        # Load Terraform state
        tfstate = load_tfstate(tfstate_file)

        # Extract and save existing resources
        existing_state = extract_resources(tfstate)
        save_existing_state(existing_state, state_file)

        # Load new resources
        repositories_json = os.getenv("REPOSITORIES", "[]")
        teams_json = os.getenv("TEAMS", "[]")
        memberships_json = os.getenv("MEMBERSHIPS", "[]")
        repo_collaborators_json = os.getenv("REPOSITORY_COLLABORATORS", "[]")

        default_repo_config = config["default_repository"]
        default_team_config = config["default_team"]
        default_membership_config = config.get("default_membership", {})
        default_repo_collaborator_config = config.get(
            "default_repository_collaborator", {})

        new_repositories = [
            Repository(
                **{**default_repo_config, **repo}
            ) for repo in json.loads(repositories_json)
        ]
        new_teams = [
            Team(
                **{**default_team_config, **team}
            ) for team in json.loads(teams_json)
        ]
        new_memberships = [
            Membership(**{**default_membership_config, **membership})
            for membership in json.loads(memberships_json)
        ]
        from models.repository_collaborator import RepositoryCollaborator
        new_repo_collaborators = [
            RepositoryCollaborator(
                **{**default_repo_collaborator_config, **collab})
            for collab in json.loads(repo_collaborators_json)
        ]
        # Calculate differences
        repos_to_add, repos_to_update, repos_to_delete = calculate_diff(
            existing_state["repositories"], new_repositories, key="repository_name"
        )
        teams_to_add, teams_to_update, teams_to_delete = calculate_diff(
            existing_state["teams"], new_teams, key="team_name"
        )
        memberships_to_add, memberships_to_update, memberships_to_delete = calculate_diff(
            existing_state.get("memberships", []), new_memberships, key="username"
        )
        repo_collaborators_to_add, repo_collaborators_to_update, repo_collaborators_to_delete = calculate_diff(
            existing_state.get("repository_collaborators", []), new_repo_collaborators, key="collaborator_id"
        )

        # Process resources
        resource_changes = ResourceChanges(
            repos_to_add, repos_to_update, repos_to_delete,
            teams_to_add, teams_to_update, teams_to_delete,
            memberships_to_add, memberships_to_update, memberships_to_delete,
            repo_collaborators_to_add, repo_collaborators_to_update, repo_collaborators_to_delete
        )
        process_resources(config["template_dir"], output_dir, resource_changes)

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"Error occurred in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
