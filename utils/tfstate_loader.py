import json
import os


def save_existing_state(state, output_file):
    """
    Save the existing state of resources to a file.

    Args:
        state (dict): The state of the resources to be saved.
        output_file (str): The file path where the state will be saved.
    """
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Existing resources saved to {output_file}")


def load_tfstate(tfstate_file):
    """
    Load the Terraform state file.

    Args:
        tfstate_file (str): The file path of the Terraform state file.

    Returns:
        dict: The loaded Terraform state.
    """
    with open(tfstate_file, "r") as f:
        return json.load(f)


def extract_resources(tfstate):
    """
    Extract resources from the Terraform state file.

    Args:
        tfstate (dict): The Terraform state.

    Returns:
        dict: A dictionary containing lists of repositories and teams.
    """
    repositories = []
    teams = []

    for resource in tfstate.get("resources", []):
        if resource["type"] == "github_repository":
            for instance in resource.get("instances", []):
                attributes = instance.get("attributes", {})
                repositories.append({
                    "repository_name": attributes["name"],
                    "description": attributes.get("description", ""),
                    "visibility": attributes["visibility"]
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

    return {"repositories": repositories, "teams": teams}
