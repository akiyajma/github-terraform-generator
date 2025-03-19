import json
import os

from loguru import logger


def save_existing_state(state, output_file):
    """
    Save the extracted state of resources to a JSON file.

    This function ensures that the specified output directory exists before writing
    the resource state as a JSON file. The saved state includes information about
    repositories, teams, memberships, and repository collaborators.

    Args:
        state (dict): The current state of resources, structured as:
            - "repositories" (list[dict]): List of repositories, each containing:
                - `repository_name` (str): Name of the repository.
                - `description` (str, optional): Repository description.
                - `visibility` (str): Visibility level ("public", "private").
                - `gitignore_template` (str, optional): Git ignore template (if any).
            - "teams" (list[dict]): List of teams, each containing:
                - `team_name` (str): Team name.
                - `description` (str, optional): Team description.
                - `privacy` (str): Privacy level ("closed", "secret").
                - `members` (list[dict], optional): List of team members (if any).
            - "memberships" (list[dict]): List of GitHub memberships, each containing:
                - `username` (str): GitHub username.
                - `role` (str): Role within the organization ("member", "admin").
            - "repository_collaborators" (list[dict]): List of repository collaborators, each containing:
                - `repository_name` (str): Repository to which the user is added.
                - `username` (str): Collaborator's GitHub username.
                - `permission` (str): Assigned permission ("pull", "push", "admin").
                - `collaborator_id` (str): Unique ID (`repository_name_username`).

        output_file (str): The file path where the extracted state will be saved.

    Raises:
        OSError: If there is an issue creating the directory or writing the file.
        Exception: If any unexpected error occurs during saving.

    Example:
        state = {
            "repositories": [{"repository_name": "repo1", "visibility": "public", "description": "A public repository"}],
            "teams": [{"team_name": "dev-team", "description": "Development team", "privacy": "closed"}],
            "memberships": [{"username": "user1", "role": "member"}],
            "repository_collaborators": [{"repository_name": "repo1", "username": "user2", "permission": "push"}]
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
    Load and parse the Terraform state file (`terraform.tfstate`) in JSON format.

    Args:
        tfstate_file (str): Path to the Terraform state file.

    Returns:
        dict: The parsed Terraform state as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified tfstate file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON content.
        Exception: If any other error occurs during file reading or parsing.

    Example:
        tfstate = load_tfstate("path/to/terraform.tfstate")
        # tfstate -> {"resources": [...], ...}
    """
    try:
        with open(tfstate_file, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Terraform state file not found: {e}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON format in {tfstate_file}: {e}", e.doc, e.pos)
    except Exception as e:
        raise Exception(f"Unexpected error loading tfstate: {e}")


def extract_resources(tfstate):
    """
    Extract repositories, teams, memberships, and repository collaborators from the Terraform state.

    This function processes the Terraform state to identify resources of type:
    - `github_repository`
    - `github_team`
    - `github_membership`
    - `github_repository_collaborator`

    It extracts relevant attributes such as repository names, team descriptions,
    user roles, and repository collaborator permissions.

    Args:
        tfstate (dict): The Terraform state dictionary, containing a `resources` key.

    Returns:
        dict: A dictionary containing:
            - "repositories" (list[dict]): List of repositories with attributes:
                - `repository_name` (str): Name of the repository.
                - `description` (str, optional): Repository description.
                - `visibility` (str): Visibility level ("public", "private").
                - `gitignore_template` (str, optional): Git ignore template (if any).
            - "teams" (list[dict]): List of teams with attributes:
                - `team_name` (str): Team name.
                - `description` (str, optional): Team description.
                - `privacy` (str): Privacy level ("closed", "secret").
                - `members` (list[dict], optional): Team members (future support).
            - "memberships" (list[dict]): List of GitHub memberships with attributes:
                - `username` (str): GitHub username.
                - `role` (str): Role within the organization ("member", "admin").
            - "repository_collaborators" (list[dict]): List of repository collaborators with attributes:
                - `repository_name` (str): Repository name.
                - `username` (str): GitHub username of the collaborator.
                - `permission` (str): Assigned permission ("pull", "push", "admin").
                - `collaborator_id` (str): Unique ID (`repository_name_username`).

    Raises:
        KeyError: If required keys are missing in the Terraform state.
        Exception: If an unexpected error occurs during extraction.

    Example:
        tfstate = {
            "resources": [
                {
                    "type": "github_repository",
                    "instances": [{"attributes": {"name": "repo1", "visibility": "public", "description": "Sample repo", "gitignore_template": "Python"}}]
                },
                {
                    "type": "github_team",
                    "instances": [{"attributes": {"name": "dev-team", "privacy": "closed", "description": "Development team"}}]
                },
                {
                    "type": "github_membership",
                    "instances": [{"attributes": {"username": "user1", "role": "member"}}]
                },
                {
                    "type": "github_repository_collaborator",
                    "instances": [{"attributes": {"repository": "repo1", "username": "user2", "permission": "push"}}]
                }
            ]
        }
        extracted = extract_resources(tfstate)
        # extracted -> {
        #     "repositories": [{"repository_name": "repo1", "description": "Sample repo", "visibility": "public", "gitignore_template": "Python"}],
        #     "teams": [{"team_name": "dev-team", "description": "Development team", "privacy": "closed"}],
        #     "memberships": [{"username": "user1", "role": "member"}],
        #     "repository_collaborators": [{"repository_name": "repo1", "username": "user2", "permission": "push", "collaborator_id": "repo1_user2"}]
        # }
    """
    try:
        repositories = []
        teams = []
        memberships = []
        repo_collaborators = []

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
                        "members": []
                    })
            elif resource["type"] == "github_membership":
                for instance in resource.get("instances", []):
                    attributes = instance.get("attributes", {})
                    memberships.append({
                        "username": attributes["username"],
                        "role": attributes["role"]
                    })
            elif resource["type"] == "github_repository_collaborator":
                for instance in resource.get("instances", []):
                    attributes = instance.get("attributes", {})
                    repo_collaborators.append({
                        "repository_name": attributes["repository"],
                        "username": attributes["username"],
                        "permission": attributes["permission"],
                        "collaborator_id": f"{attributes['repository']}_{attributes['username']}"
                    })

        return {"repositories": repositories, "teams": teams, "memberships": memberships, "repository_collaborators": repo_collaborators}
    except KeyError as e:
        raise KeyError(f"Missing expected key in tfstate: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error extracting resources: {e}")
