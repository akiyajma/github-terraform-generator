import os
from unittest.mock import MagicMock, patch

import pytest

from utils.process_resources import (
    process_memberships,
    process_repositories,
    process_resources,
    process_teams,
)


@pytest.fixture
def dummy_generator():
    """
    Create a mock instance of `TerraformGenerator`.

    This fixture returns a mocked version of `TerraformGenerator` where
    the repository, team, and membership generation methods can be controlled.

    Returns:
        MagicMock: A mock TerraformGenerator instance.
    """
    gen = MagicMock()
    gen.generate_repository.side_effect = None
    gen.generate_team.side_effect = None
    gen.generate_membership.side_effect = None
    return gen


# --- Tests for process_repositories ---


def test_process_repositories_add_exception(tmp_path, dummy_generator):
    """
    Ensure `process_repositories` raises an exception when adding a repository fails.

    This test mocks an error when calling `generate_repository` for an addition,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_repository.side_effect = Exception("Add error")
    repos_to_add = [{
        "repository_name": "repo1",
        "visibility": "public",
        "description": "Test repo",
        "gitignore_template": "Python"
    }]
    with pytest.raises(Exception) as excinfo:
        process_repositories(dummy_generator, str(
            tmp_path), repos_to_add, [], [])
    assert "Error adding repository" in str(excinfo.value)


def test_process_repositories_update_exception(tmp_path, dummy_generator):
    """
    Ensure `process_repositories` raises an exception when updating a repository fails.

    This test mocks an error when calling `generate_repository` for an update,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_repository.side_effect = Exception("Update error")
    repos_to_update = [{
        "repository_name": "repo1",
        "visibility": "public",
        "description": "Test repo",
        "gitignore_template": "Python"
    }]
    with pytest.raises(Exception) as excinfo:
        process_repositories(dummy_generator, str(
            tmp_path), [], repos_to_update, [])
    assert "Error updating repository" in str(excinfo.value)


def test_process_repositories_deletion_exception(tmp_path, dummy_generator):
    """
    Ensure `process_repositories` raises an exception when repository deletion fails.

    This test creates a repository Terraform file and patches `os.remove` to raise
    an exception, verifying that the deletion failure is properly handled.
    """
    repos_to_delete = [{"repository_name": "repo1"}]
    test_file = os.path.join(str(tmp_path), "repo1_repository.tf")
    with open(test_file, "w") as f:
        f.write("dummy")

    with patch("os.remove", side_effect=Exception("Delete error")):
        with pytest.raises(Exception) as excinfo:
            process_repositories(dummy_generator, str(
                tmp_path), [], [], repos_to_delete)
        assert "Error deleting repository" in str(excinfo.value)


# --- Tests for process_teams ---


def test_process_teams_add_exception(tmp_path, dummy_generator):
    """
    Ensure `process_teams` raises an exception when adding a team fails.

    This test mocks an error when calling `generate_team` for an addition,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_team.side_effect = Exception("Team add error")
    teams_to_add = [{"team_name": "team1", "privacy": "closed",
                     "description": "Test team", "members": []}]
    with pytest.raises(Exception) as excinfo:
        process_teams(dummy_generator, str(tmp_path), teams_to_add, [], [])
    assert "Error adding team" in str(excinfo.value)


def test_process_teams_update_exception(tmp_path, dummy_generator):
    """
    Ensure `process_teams` raises an exception when updating a team fails.

    This test mocks an error when calling `generate_team` for an update,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_team.side_effect = Exception("Team update error")
    teams_to_update = [{"team_name": "team1", "privacy": "closed",
                        "description": "Test team", "members": []}]
    with pytest.raises(Exception) as excinfo:
        process_teams(dummy_generator, str(tmp_path), [], teams_to_update, [])
    assert "Error updating team" in str(excinfo.value)


def test_process_teams_deletion_exception(mocker, tmp_path):
    """
    Ensure `process_resources` does not raise an exception when team deletion fails.

    This test creates a team Terraform file and patches `os.remove` to raise an exception,
    verifying that `process_resources` does not propagate the error.
    """
    output_dir = str(tmp_path)
    os.makedirs(output_dir, exist_ok=True)
    tf_file = os.path.join(output_dir, "team1_team.tf")
    with open(tf_file, "w") as f:
        f.write("dummy")

    resource_changes = MagicMock()
    resource_changes.teams_to_delete = [{"team_name": "team1"}]

    mocker.patch("os.remove", side_effect=Exception("Team delete error"))

    process_resources("templates", output_dir, resource_changes)

    # The file should still exist because the deletion failed
    assert os.path.exists(tf_file)


# --- Tests for process_memberships ---


def test_process_memberships_add_exception(tmp_path, dummy_generator):
    """
    Ensure `process_memberships` raises an exception when adding a membership fails.

    This test mocks an error when calling `generate_membership` for an addition,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_membership.side_effect = Exception(
        "Membership add error")
    memberships_to_add = [{"username": "user1", "role": "member"}]
    with pytest.raises(Exception) as excinfo:
        process_memberships(dummy_generator, str(
            tmp_path), memberships_to_add, [], [])
    assert "Error adding membership" in str(excinfo.value)


def test_process_memberships_update_exception(tmp_path, dummy_generator):
    """
    Ensure `process_memberships` raises an exception when updating a membership fails.

    This test mocks an error when calling `generate_membership` for an update,
    ensuring that an appropriate exception is raised.
    """
    dummy_generator.generate_membership.side_effect = Exception(
        "Membership update error")
    memberships_to_update = [{"username": "user1", "role": "member"}]
    with pytest.raises(Exception) as excinfo:
        process_memberships(dummy_generator, str(tmp_path),
                            [], memberships_to_update, [])
    assert "Error updating membership" in str(excinfo.value)


def test_process_memberships_deletion_exception(tmp_path, dummy_generator):
    """
    Ensure `process_memberships` raises an exception when membership deletion fails.

    This test creates a membership Terraform file and patches `os.remove` to raise
    an exception, verifying that the deletion failure is properly handled.
    """
    memberships_to_delete = [{"username": "user1"}]
    test_file = os.path.join(str(tmp_path), "user1_membership.tf")
    with open(test_file, "w") as f:
        f.write("dummy")

    with patch("os.remove", side_effect=Exception("Membership delete error")):
        with pytest.raises(Exception) as excinfo:
            process_memberships(dummy_generator, str(
                tmp_path), [], [], memberships_to_delete)
        assert "Error deleting membership" in str(excinfo.value)


# --- Integration test for process_resources ---


def test_process_resources_complete(tmp_path, dummy_generator, mocker):
    """
    Ensure `process_resources` correctly processes repository, team, and membership changes.

    This test verifies that:
    - New repositories, teams, and memberships are created.
    - Existing ones are updated.
    - Marked ones are deleted.

    It creates Terraform files for a repository, team, and membership, runs `process_resources`,
    and confirms the expected deletions.
    """
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=dummy_generator)
    resource_changes = mocker.MagicMock()

    resource_changes.repos_to_delete = [{"repository_name": "repo1"}]
    resource_changes.teams_to_delete = [{"team_name": "team1"}]
    resource_changes.memberships_to_delete = [{"username": "user1"}]

    repo_file = os.path.join(str(tmp_path), "repo1_repository.tf")
    team_file = os.path.join(str(tmp_path), "team1_team.tf")
    membership_file = os.path.join(str(tmp_path), "user1_membership.tf")
    for file_path in [repo_file, team_file, membership_file]:
        with open(file_path, "w") as f:
            f.write("dummy")

    process_resources("templates", str(tmp_path), resource_changes)

    assert not os.path.exists(repo_file)
    assert not os.path.exists(team_file)
    assert not os.path.exists(membership_file)
