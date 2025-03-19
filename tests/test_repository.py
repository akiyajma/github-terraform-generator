import pytest
from pydantic import ValidationError

from models.repository import Repository


def test_repository_model_valid():
    """
    Test that a valid `Repository` model is created successfully.

    This test ensures that:
    - The model correctly initializes with the provided attributes.
    - The `repository_name`, `visibility`, and `gitignore_template` are properly set.
    """
    data = {
        "repository_name": "repo1",
        "description": "Repo1 description",
        "visibility": "public",
        "gitignore_template": "Python"
    }
    repo = Repository(**data)
    assert repo.repository_name == "repo1"
    assert repo.visibility == "public"
    assert repo.gitignore_template == "Python"


def test_repository_model_invalid_visibility():
    """
    Test that a `ValidationError` is raised for an invalid `visibility` value.

    This test verifies that providing an unsupported `visibility` value
    (not "public", "private", or "internal") triggers a validation error.
    """
    data = {
        "repository_name": "repo1",
        "description": "Repo1 description",
        "visibility": "invalid",
        "gitignore_template": "Python"
    }
    with pytest.raises(ValidationError):
        Repository(**data)
