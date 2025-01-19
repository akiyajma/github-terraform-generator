import json
import os

from loguru import logger


def save_existing_state(state, output_file):
    """
    Save the current state of resources to a file in JSON format.

    This function ensures the output directory exists and writes the given state
    as a JSON file to the specified file path. The state typically includes details
    about repositories (e.g., `repository_name`, `description`, `gitignore_template`)
    and teams.

    Args:
        state (dict): The current state of resources to be saved, including:
            - "repositories" (list[dict]): Each repository dictionary may contain:
                - `repository_name` (str): The name of the repository.
                - `description` (str): A description of the repository.
                - `visibility` (str): The visibility of the repository.
                - `gitignore_template` (str, optional): A `.gitignore` template, if applicable.
            - "teams" (list[dict]): Each team dictionary may contain:
                - `team_name` (str): The name of the team.
                - `description` (str): A description of the team.
                - `privacy` (str): The privacy setting of the team.
        output_file (str): The file path where the state will be saved.

    Raises:
        OSError: If there is an error creating the output directory or writing the file.
        Exception: For other unexpected errors during the save operation.

    Example:
        state = {
            "repositories": [{"repository_name": "repo1", "visibility": "public", "description": "A public repo"}],
            "teams": [{"team_name": "team1", "description": "A new team", "privacy": "closed"}]
        }
        save_existing_state(state, "output/existing_state.json")
    """
    try:
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(state, f, indent=2)
        logger.info(f"Existing resources saved to {output_file}")
    except OSError as e:
        raise OSError(f"Failed to save existing state to {output_file}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error saving existing state: {e}")


def load_tfstate(tfstate_file):
    """
    Load and parse the Terraform state file in JSON format.

    Args:
        tfstate_file (str): The file path to the Terraform state file.

    Returns:
        dict: The parsed Terraform state as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified tfstate file does not exist.
        json.JSONDecodeError: If the tfstate file contains invalid JSON content.
        Exception: For other unexpected errors during file reading or parsing.

    Example:
        tfstate = load_tfstate("path/to/terraform.tfstate")
        # tfstate -> {"resources": [...], ...}
    """
    try:
        with open(tfstate_file, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"tfstate file not found: {e}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON format in {tfstate_file}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error loading tfstate: {e}")


def extract_resources(tfstate):
    """
    Extract lists of repositories and teams from the Terraform state.

    This function processes the Terraform state dictionary and identifies
    resources of type `github_repository` and `github_team`, extracting their
    relevant attributes such as `repository_name`, `description`, `gitignore_template`, etc.

    Args:
        tfstate (dict): The Terraform state dictionary, typically containing
            a `resources` key with a list of resource definitions.

    Returns:
        dict: A dictionary containing two keys:
            - "repositories" (list[dict]): A list of repositories, where each dictionary includes:
                - `repository_name` (str): The name of the repository.
                - `description` (str, optional): A description of the repository.
                - `visibility` (str): The visibility of the repository (e.g., "public", "private").
                - `gitignore_template` (str, optional): A `.gitignore` template, if applicable.
            - "teams" (list[dict]): A list of teams, where each dictionary includes:
                - `team_name` (str): The name of the team.
                - `description` (str, optional): A description of the team.
                - `privacy` (str): The privacy level of the team (e.g., "closed", "secret").
                - `members` (list[dict], optional): Team members (future support).

    Raises:
        KeyError: If expected keys are missing in the Terraform state.
        Exception: For other unexpected errors during resource extraction.

    Example:
        tfstate = {
            "resources": [
                {
                    "type": "github_repository",
                    "instances": [{"attributes": {"name": "repo1", "visibility": "public", "description": "Sample repo", "gitignore_template": "Python"}}]
                },
                {
                    "type": "github_team",
                    "instances": [{"attributes": {"name": "team1", "privacy": "closed", "description": "Dev team"}}]
                }
            ]
        }
        resources = extract_resources(tfstate)
        # resources -> {
        #     "repositories": [{"repository_name": "repo1", "description": "Sample repo", "visibility": "public", "gitignore_template": "Python"}],
        #     "teams": [{"team_name": "team1", "description": "Dev team", "privacy": "closed"}]
        # }
    """
    try:
        repositories = []
        teams = []

        for resource in tfstate.get("resources", []):
            if resource["type"] == "github_repository":
                for instance in resource.get("instances", []):
                    attributes = instance.get("attributes", {})
                    repositories.append({
                        "repository_name": attributes["name"],
                        "description": attributes.get("description", ""),
                        "visibility": attributes["visibility"],
                        "gitignore_template": attributes.get("gitignore_template", None)
                    })
            elif resource["type"] == "github_team":
                for instance in resource.get("instances", []):
                    attributes = instance.get("attributes", {})
                    teams.append({
                        "team_name": attributes["name"],
                        "description": attributes.get("description", ""),
                        "privacy": attributes["privacy"],
                        "members": []  # Add members if present in future requirements
                    })

        return {"repositories": repositories, "teams": teams}
    except KeyError as e:
        raise KeyError(f"Missing expected key in tfstate: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error extracting resources: {e}")
