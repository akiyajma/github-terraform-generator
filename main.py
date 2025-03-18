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
    Main function to process and apply changes to the Terraform state.

    This function serves as the entry point for managing resources defined in Terraform state.
    It performs the following steps:
    1. Loads the application configuration from `config.yaml`.
    2. Loads the existing Terraform state from the specified file.
    3. Extracts resources (repositories, teams, and memberships) from the Terraform state.
    4. Compares the extracted resources with the new resources provided via environment variables,
       applying default values from `config.yaml` where applicable.
    5. Calculates the differences (additions, updates, deletions) between the existing and new resources.
    6. Applies the changes by generating, updating, or deleting Terraform files.

    Args:
        output_dir_override (str, optional): Overrides the output directory specified in the configuration.
            If not provided, the output directory specified in `config.yaml` is used.

    Environment Variables:
        REPOSITORIES (str): A JSON-encoded list of repository definitions. Each repository should include:
            - `repository_name` (str): The name of the repository.
            - `description` (str, optional): A description of the repository.
            - `visibility` (str): The visibility of the repository (e.g., "public" or "private").
            - `gitignore_template` (str, optional): The Git ignore template to apply.
              If set to "None", this attribute will be excluded from the generated Terraform configuration.
        TEAMS (str): A JSON-encoded list of team definitions. Each team should include:
            - `team_name` (str): The name of the team.
            - `description` (str, optional): A description of the team.
            - `privacy` (str): The privacy level of the team (e.g., "closed" or "secret").
            - `members` (list[dict], optional): A list of team members with their roles.
        MEMBERSHIPS (str): A JSON-encoded list of GitHub usernames for organization membership.
            - Each username is assigned the role "member".

    Configuration:
        The application configuration (`config.yaml`) includes:
        - `default_repository` (dict): Default values for repository attributes, applied if not explicitly provided.
        - `default_team` (dict): Default values for team attributes, applied if not explicitly provided.

    Raises:
        SystemExit: Exits the script with status code 1 if an unhandled error occurs.

    Logs:
        - Logs informational messages about the processing steps.
        - Logs errors with details if any step fails.

    Example:
        To override the output directory and process changes:
        >>> main(output_dir_override="/custom/output/dir")

    Files Used:
        - Configuration: `config/config.yaml`
        - Terraform state: `<output_dir>/terraform.tfstate`
        - Resource changes are saved to `<output_dir>/existing_resources.json`.

    Notes:
        - The `gitignore_template` field in repositories is conditionally included based on its value.
          If the value is "None", it will be excluded from the generated Terraform configuration.
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

        # Load new resources from environment variables
        repositories_json = os.getenv("REPOSITORIES", "[]")
        teams_json = os.getenv("TEAMS", "[]")
        memberships_json = os.getenv("MEMBERSHIPS", "[]")

        default_repo_config = config["default_repository"]
        default_team_config = config["default_team"]

        # Parse JSON and apply default values
        new_repositories = [
            Repository(**{**default_repo_config, **repo})
            for repo in json.loads(repositories_json)
        ]
        new_teams = [
            Team(**{**default_team_config, **team})
            for team in json.loads(teams_json)
        ]

        # --- Memberships Handling ---
        # Ensure existing memberships is a valid list
        existing_memberships = existing_state.get("memberships", [])
        if not isinstance(existing_memberships, list):
            existing_memberships = []

        # Ensure all elements in existing_memberships are dictionaries
        existing_memberships = [
            m for m in existing_memberships if isinstance(m, dict)]

        # Convert new memberships from environment variable
        new_memberships = [Membership(username=membership)
                           for membership in json.loads(memberships_json)]
        new_memberships_dicts = [membership.to_dict()
                                 for membership in new_memberships]

        # Calculate differences for repositories, teams, and memberships
        repos_to_add, repos_to_update, repos_to_delete = calculate_diff(
            existing_state.get("repositories", []), new_repositories, key="repository_name"
        )
        teams_to_add, teams_to_update, teams_to_delete = calculate_diff(
            existing_state.get("teams", []), new_teams, key="team_name"
        )
        memberships_to_add, memberships_to_update, memberships_to_delete = calculate_diff(
            existing_memberships, new_memberships_dicts, key="username"
        )

        # Process resources including memberships with full lifecycle (add/update/delete)
        resource_changes = ResourceChanges(
            repos_to_add, repos_to_update, repos_to_delete,
            teams_to_add, teams_to_update, teams_to_delete,
            memberships_to_add, memberships_to_update, memberships_to_delete
        )
        process_resources(config["template_dir"], output_dir, resource_changes)

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"Error occurred in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
