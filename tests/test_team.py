import pytest
from pydantic import ValidationError

from models.team import Team


def test_team_model_valid():
    """
    Test that a valid `Team` model is created successfully.

    This test ensures that:
    - The model correctly initializes with the provided attributes.
    - The `team_name`, `privacy`, and `members` are properly set.
    - The `members` list contains valid `TeamMember` objects with expected attributes.
    """
    data = {
        "team_name": "team1",
        "description": "Team1 description",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "maintainer"}]
    }
    team = Team(**data)
    assert team.team_name == "team1"
    assert team.privacy == "closed"

    # Ensure members are correctly converted into Pydantic models
    assert hasattr(team.members[0], "username")
    assert team.members[0].username == "user1"


def test_team_model_invalid_member_role():
    """
    Test that a `ValidationError` is raised for an invalid member `role`.

    This test verifies that providing an unsupported `role` value
    (not "member" or "maintainer") triggers a validation error.
    """
    data = {
        "team_name": "team1",
        "description": "Team1 description",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "invalid"}]
    }
    with pytest.raises(ValidationError):
        Team(**data)
