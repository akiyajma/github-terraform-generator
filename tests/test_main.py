import json
import os
import re

import pytest

from main import main


@pytest.fixture
def mock_config_file(tmpdir):
    """
    Create a mock configuration file for testing.

    This fixture generates a temporary `config.yaml` file containing default settings
    for repositories (e.g., `visibility`) and teams (e.g., `privacy`, `role`) to be used
    during tests.

    Returns:
        str: The file path to the mock configuration file.
    """
    config_path = tmpdir.join("config.yaml")
    return str(config_path)


@pytest.fixture
def create_tfstate_file(tmpdir):
    """
    Create a mock Terraform state file for testing.

    This fixture generates a temporary `terraform.tfstate` file with sample resources,
    including one GitHub repository and one GitHub team, to simulate an existing state.

    Returns:
        str: The file path to the mock Terraform state file.
    """
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
    Test the addition of a new repository.

    This test verifies that the `main` function correctly identifies a new repository
    (with attributes such as `repository_name`, `description`, and `gitignore_template`)
    in the requested state and generates a corresponding Terraform configuration file.

    Steps:
    1. Mock the `REPOSITORIES` environment variable with a new repository definition.
    2. Ensure no teams are modified (`TEAMS` is empty).
    3. Execute the `main` function.
    4. Verify that the new repository Terraform file is generated.
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
    Test the update of an existing repository.

    This test verifies that the `main` function detects attribute changes (e.g., `description`,
    `visibility`) in an existing repository and updates the corresponding Terraform
    configuration file.

    Steps:
    1. Mock the `REPOSITORIES` environment variable with an updated repository definition.
    2. Ensure no teams are modified (`TEAMS` is empty).
    3. Execute the `main` function.
    4. Verify that the repository Terraform file reflects the updated attributes.
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
    Test the deletion of a repository.

    This test verifies that the `main` function identifies repositories present in the
    existing state but not in the requested state and deletes the corresponding
    Terraform configuration files.

    Steps:
    1. Mock the `REPOSITORIES` environment variable with no repositories.
    2. Ensure no teams are modified (`TEAMS` is empty).
    3. Execute the `main` function.
    4. Verify that the repository Terraform file is deleted.
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
    Test the addition of a new team.

    This test verifies that the `main` function correctly identifies a new team
    (with attributes such as `team_name`, `description`, and `privacy`) in the requested
    state and generates a corresponding Terraform configuration file.

    Steps:
    1. Mock the `TEAMS` environment variable with a new team definition.
    2. Ensure no repositories are modified (`REPOSITORIES` is empty).
    3. Execute the `main` function.
    4. Verify that the new team Terraform file is generated.
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
    Test the update of an existing team.

    This test verifies that the `main` function detects attribute changes (e.g.,
    `description`, `privacy`) in an existing team and updates the corresponding Terraform
    configuration file.

    Steps:
    1. Mock the `TEAMS` environment variable with an updated team definition.
    2. Ensure no repositories are modified (`REPOSITORIES` is empty).
    3. Execute the `main` function.
    4. Verify that the team Terraform file reflects the updated attributes.
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
    Test the deletion of a team.

    This test verifies that the `main` function identifies teams present in the existing
    state but not in the requested state and deletes the corresponding Terraform
    configuration files.

    Steps:
    1. Mock the `TEAMS` environment variable with no teams.
    2. Ensure no repositories are modified (`REPOSITORIES` is empty).
    3. Execute the `main` function.
    4. Verify that the team Terraform file is deleted.
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
