import json
import os
import sys

from loguru import logger

from config.config_loader import load_config
from logging_config import setup_logging
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
    3. Extracts resources (repositories and teams) from the Terraform state.
    4. Compares the extracted resources with the new resources provided via environment variables.
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
        TEAMS (str): A JSON-encoded list of team definitions. Each team should include:
            - `team_name` (str): The name of the team.
            - `description` (str, optional): A description of the team.
            - `privacy` (str): The privacy level of the team (e.g., "closed" or "secret").
            - `members` (list[dict], optional): A list of team members with their roles.

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
        new_repositories = []
        if repositories_json.strip():
            new_repositories = [Repository(**repo)
                                for repo in json.loads(repositories_json)]
        new_teams = []
        if teams_json.strip():
            new_teams = [Team(**team) for team in json.loads(teams_json)]

        # Calculate differences
        repos_to_add, repos_to_update, repos_to_delete = calculate_diff(
            existing_state["repositories"], new_repositories, key="repository_name"
        )
        teams_to_add, teams_to_update, teams_to_delete = calculate_diff(
            existing_state["teams"], new_teams, key="team_name"
        )

        # Process resources
        resource_changes = ResourceChanges(
            repos_to_add, repos_to_update, repos_to_delete,
            teams_to_add, teams_to_update, teams_to_delete
        )
        process_resources(config["template_dir"], output_dir, resource_changes)

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"Error occurred in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
