import json
import os

import pytest

from config.config_loader import load_config
from main import main
from utils.tfstate_loader import load_tfstate, save_existing_state


@pytest.fixture
def mock_config_file(tmpdir):
    """Create a mock configuration file for testing"""
    config_content = """
    template_dir: "templates"
    output_dir: "terraform"
    tfstate_file: "terraform.tfstate"
    state_file: "existing_resources.json"
    default_repository:
      visibility: "public"
    default_team:
      privacy: "closed"
      role: "member"
    """
    config_path = tmpdir.join("config.yaml")
    config_path.write(config_content)
    return str(config_path)


def test_main(monkeypatch, tmpdir, mock_config_file):
    """
    Test the main function.

    Test Cases:
    1. Verify that the tfstate file is correctly loaded.
    2. Verify that the existing state is correctly saved to a file.
    3. Verify that the generated Terraform files for repositories and teams are created in the output directory.
    """
    repositories = [
        {"repository_name": "test-repo", "description": "Test repository",
            "visibility": "public", "gitignore_template": "Python"}
    ]
    teams = [
        {"team_name": "test-team", "description": "Test team", "privacy": "closed",
            "members": [{"username": "user1", "role": "maintainer"}]}
    ]
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    # Monkeypatch `load_config` to return the mock configuration file
    def mock_load_config():
        return load_config(mock_config_file)

    monkeypatch.setattr("main.load_config", mock_load_config)

    # Create a mock tfstate file
    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_file = tmp_terraform_dir.join("terraform.tfstate")
    existing_tfstate = {
        "resources": []
    }
    tfstate_file.write(json.dumps(existing_tfstate))

    # Monkeypatch `load_tfstate`
    def mock_load_tfstate(file_path):
        if file_path == os.path.join(str(tmp_terraform_dir), "terraform.tfstate"):
            return load_tfstate(str(tfstate_file))
        raise FileNotFoundError(file_path)

    monkeypatch.setattr("main.load_tfstate", mock_load_tfstate)

    # Create a temporary existing state file for testing
    existing_state_file = tmp_terraform_dir.join("existing_resources.json")
    existing_state = {"repositories": [], "teams": []}
    save_existing_state(existing_state, str(existing_state_file))

    # Execute the test target (set the output directory to the temporary directory)
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify the results
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "test-repo_repository.tf" in output_files
    assert "test-team_team.tf" in output_files
