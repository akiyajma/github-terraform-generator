import json
import os
import re

import pytest

from main import main


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


@pytest.fixture
def create_tfstate_file(tmpdir):
    """Fixture to create a mock Terraform state file."""
    tfstate_path = tmpdir.join("terraform.tfstate")
    tfstate_content = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            "name": "repo1",
                            "visibility": "public",
                            "gitignore_template": "Python"
                        }
                    }
                ]
            },
            {
                "type": "github_team",
                "instances": [
                    {
                        "attributes": {
                            "name": "team1",
                            "description": "Test team",
                            "privacy": "closed"
                        }
                    }
                ]
            }
        ]
    }
    tfstate_path.write(json.dumps(tfstate_content))
    return str(tfstate_path)


def test_main_repo_addition(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with repository addition.
    """
    repositories = [
        {"repository_name": "new-repo", "description": "New repository",
         "visibility": "public", "gitignore_template": "Go"}
    ]
    teams = []  # No changes to teams
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify addition
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "new-repo_repository.tf" in output_files


def test_main_repo_update(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with repository update.
    """
    repositories = [
        {"repository_name": "repo1", "description": "Updated repository",
         "visibility": "private", "gitignore_template": "Python"}
    ]
    teams = []  # No changes to teams
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify update
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "repo1_repository.tf" in output_files
    with open(os.path.join(tmp_terraform_dir, "repo1_repository.tf"), "r") as f:
        content = f.read()
        assert re.search(r'description\s*=\s*"Updated repository"', content)
        assert re.search(r'visibility\s*=\s*"private"', content)


def test_main_repo_deletion(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with repository deletion.
    """
    repositories = []  # No repositories requested
    teams = []  # No changes to teams
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify deletion
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "repo1_repository.tf" not in output_files


def test_main_team_addition(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with team addition.
    """
    repositories = []  # No changes to repositories
    teams = [
        {"team_name": "new-team", "description": "New team", "privacy": "secret",
         "members": [{"username": "user1", "role": "maintainer"}]}
    ]
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify addition
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "new-team_team.tf" in output_files


def test_main_team_update(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with team update.
    """
    repositories = []  # No changes to repositories
    teams = [
        {"team_name": "team1", "description": "Updated team", "privacy": "secret",
         "members": [{"username": "user1", "role": "maintainer"}]}
    ]
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify update
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "team1_team.tf" in output_files
    with open(os.path.join(tmp_terraform_dir, "team1_team.tf"), "r") as f:
        content = f.read()
        assert re.search(r'description\s*=\s*"Updated team"', content)
        assert re.search(r'privacy\s*=\s*"secret"', content)


def test_main_team_deletion(monkeypatch, tmpdir, create_tfstate_file):
    """
    Test the main function with team deletion.
    """
    repositories = []  # No changes to repositories
    teams = []  # No teams requested
    monkeypatch.setenv("REPOSITORIES", json.dumps(repositories))
    monkeypatch.setenv("TEAMS", json.dumps(teams))

    tmp_terraform_dir = tmpdir.mkdir("terraform")
    tfstate_path = os.path.join(tmp_terraform_dir, "terraform.tfstate")
    os.rename(create_tfstate_file, tfstate_path)

    # Execute main
    main(output_dir_override=str(tmp_terraform_dir))

    # Verify deletion
    output_files = os.listdir(str(tmp_terraform_dir))
    assert "team1_team.tf" not in output_files
