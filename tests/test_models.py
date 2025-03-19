import pytest
from pydantic import ValidationError

from models.membership import Membership
from models.repository import Repository
from models.repository_collaborator import RepositoryCollaborator
from models.team import Team

# ----- Repository Model Tests -----


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


# ----- Team Model Tests -----

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
    assert team.privacy == "closed"
    assert team.members[0].username == "user1"
    assert team.members[0].role == "maintainer"


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


# ----- Membership Model Tests -----

def test_membership_model_valid():
    """
    Test the Membership model with valid data.

    Test Cases:
    1. Verify that a Membership object is created with the correct attributes.
    """
    data = {
        "username": "test-user",
        "role": "admin"
    }
    membership = Membership(**data)
    assert membership.username == "test-user"
    assert membership.role == "admin"
    assert membership.allow_delete is False


def test_membership_model_invalid_role():
    """
    Test the Membership model with an invalid role.

    Test Cases:
    1. Verify that a ValidationError is raised when an invalid role is provided.
    """
    data = {
        "username": "test-user",
        "role": "invalid"  # Invalid role
    }
    with pytest.raises(ValidationError):
        Membership(**data)


# ----- Repository Collaborator Model Tests -----

def test_repository_collaborator_model_valid():
    """
    Test the RepositoryCollaborator model with valid data.

    Test Cases:
    1. Verify that a RepositoryCollaborator object is created with the correct attributes.
    """
    data = {
        "repository_name": "test-repo",
        "username": "collaborator-user",
        "permission": "push"
    }
    collaborator = RepositoryCollaborator(**data)
    assert collaborator.repository_name == "test-repo"
    assert collaborator.username == "collaborator-user"
    assert collaborator.permission == "push"
    assert collaborator.allow_delete is False
    assert collaborator.collaborator_id == "test-repo_collaborator-user"


def test_repository_collaborator_model_invalid_permission():
    """
    Test the RepositoryCollaborator model with an invalid permission.

    Test Cases:
    1. Verify that a ValidationError is raised when an invalid permission is provided.
    """
    data = {
        "repository_name": "test-repo",
        "username": "collaborator-user",
        "permission": "invalid"  # Invalid permission
    }
    with pytest.raises(ValidationError):
        RepositoryCollaborator(**data)
