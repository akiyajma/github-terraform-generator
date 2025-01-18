import pytest
from pydantic import ValidationError

from models.repository import Repository
from models.team import Team


def test_repository_model_valid():
    """
    Test the Repository model with valid data.

    Test Cases:
    1. Verify that a Repository object is created with the correct attributes.
    """
    data = {
        "repository_name": "test-repo",
        "description": "Test repository",
        "visibility": "public",
        "gitignore_template": "Python"
    }
    repo = Repository(**data)
    assert repo.repository_name == "test-repo"
    assert repo.visibility == "public"
    assert repo.gitignore_template == "Python"


def test_repository_model_invalid_visibility():
    """
    Test the Repository model with invalid visibility.

    Test Cases:
    1. Verify that a ValidationError is raised when an invalid visibility is provided.
    """
    data = {
        "repository_name": "test-repo",
        "description": "Test repository",
        "visibility": "invalid",
        "gitignore_template": "Python"
    }
    with pytest.raises(ValidationError):
        Repository(**data)


def test_team_model_valid():
    """
    Test the Team model with valid data.

    Test Cases:
    1. Verify that a Team object is created with the correct attributes.
    """
    data = {
        "team_name": "test-team",
        "description": "Test team",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "maintainer"}]
    }
    team = Team(**data)
    assert team.team_name == "test-team"
    assert team.members[0].username == "user1"


def test_team_model_invalid_member_role():
    """
    Test the Team model with an invalid member role.

    Test Cases:
    1. Verify that a ValidationError is raised when an invalid member role is provided.
    """
    data = {
        "team_name": "test-team",
        "description": "Test team",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "invalid"}]
    }
    with pytest.raises(ValidationError):
        Team(**data)
