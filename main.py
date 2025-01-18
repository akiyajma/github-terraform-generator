import json
import os

from config.config_loader import load_config
from logging_config import setup_logging
from models.repository import Repository
from models.team import Team
from utils.diff_calculator import calculate_diff
from utils.process_resources import process_resources
from utils.resource_changes import ResourceChanges
from utils.tfstate_loader import extract_resources, load_tfstate, save_existing_state

setup_logging()


def main(output_dir_override=None):
    """
    Main function to process the Terraform state and apply changes.

    Args:
        output_dir_override (str, optional): Override the output directory specified in the config. Defaults to None.
    """

    config = load_config()
    output_dir = output_dir_override or config["output_dir"]

    # Define the path to the tfstate file and the state file
    tfstate_file = os.path.join(output_dir, config["tfstate_file"])
    state_file = os.path.join(output_dir, config["state_file"])

    # Load the tfstate file and extract existing resources
    tfstate = load_tfstate(tfstate_file)
    existing_state = extract_resources(tfstate)

    # Save the extracted existing state to the state file
    save_existing_state(existing_state, state_file)

    # Load repositories and teams from environment variables
    repositories_json = os.getenv("REPOSITORIES", "[]")
    teams_json = os.getenv("TEAMS", "[]")
    new_repositories = [Repository(**repo)
                        for repo in json.loads(repositories_json)]
    new_teams = [Team(**team) for team in json.loads(teams_json)]

    # Calculate the differences between existing and new repositories and teams
    repos_to_add, repos_to_update, repos_to_delete = calculate_diff(
        existing_state["repositories"], new_repositories, key="repository_name"
    )
    teams_to_add, teams_to_update, teams_to_delete = calculate_diff(
        existing_state["teams"], new_teams, key="team_name"
    )

    # Create a ResourceChanges object to hold the changes
    resource_changes = ResourceChanges(
        repos_to_add, repos_to_update, repos_to_delete,
        teams_to_add, teams_to_update, teams_to_delete
    )

    # Process the resources using the template directory and output directory
    process_resources(config["template_dir"], output_dir, resource_changes)


if __name__ == "__main__":
    main()
