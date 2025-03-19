import json
import os

from main import main  # Importing main.py

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check if config.yaml exists
config_path = os.path.join(BASE_DIR, "config/config.yaml")
if not os.path.exists(config_path):
    # Create config.yaml with default settings
    with open(config_path, "w") as f:
        f.write("""\
template_dir: "templates"
output_dir: "terraform"
default_repository:
  visibility: "public"
default_team:
  privacy: "closed"
  role: "member"
default_membership:
  role: "member"
default_repository_collaborator:
  permission: "pull"
""")

# Check if the Terraform state file exists
terraform_dir = os.path.join(BASE_DIR, "terraform")
os.makedirs(terraform_dir, exist_ok=True)  # Ensure the directory exists
tfstate_path = os.path.join(terraform_dir, "terraform.tfstate")
if not os.path.exists(tfstate_path):
    # Create a new terraform.tfstate file with an initial empty state
    with open(tfstate_path, "w") as f:
        f.write(json.dumps({
            "version": 4,
            "terraform_version": "1.4.5",
            "resources": []
        }))

# Set environment variables for repositories
os.environ["REPOSITORIES"] = json.dumps([
    {
        "repository_name": "repo1",
        "description": "This is repo1",
        "visibility": "public",
        "gitignore_template": "Python"
    }
])

# Set environment variables for teams
os.environ["TEAMS"] = json.dumps([
    {
        "team_name": "team1",
        "description": "Updated team",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "maintainer"}]
    }
])

# Add memberships (all users as "member")
os.environ["MEMBERSHIPS"] = json.dumps([
    {"username": "user1", "role": "member"},
    {"username": "user2", "role": "member"},
    {"username": "user3", "role": "member"}
])

# Add external collaborators
os.environ["REPOSITORY_COLLABORATORS"] = json.dumps([
    {
        "repository_name": "repo1",
        "username": "external_user1",
        "permission": "push"
    },
    {
        "repository_name": "repo1",
        "username": "external_user2",
        "permission": "pull"
    }
])

# Change working directory to the project root
os.chdir(BASE_DIR)

# Execute main.py
if __name__ == "__main__":
    # If needed, specify a custom output directory
    custom_output_dir = os.path.join(BASE_DIR, "terraform")
    main(output_dir_override=custom_output_dir)
