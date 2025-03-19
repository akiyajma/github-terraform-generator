import pytest

from models.repository import Repository
from utils.diff_calculator import calculate_diff


def test_calculate_diff_add_update_delete():
    """
    Test the calculate_diff function with add, update, and delete cases.
    """
    existing = [
        {"repository_name": "repo1", "description": "Old repo1",
         "visibility": "public", "gitignore_template": "Python"},
        {"repository_name": "repo2", "description": "Old repo2",
         "visibility": "private", "gitignore_template": "Node"},
    ]
    requested = [
        Repository(repository_name="repo1", description="New repo1",
                   visibility="private", gitignore_template="Python"),
        Repository(repository_name="repo3", description="New repo3",
                   visibility="public", gitignore_template="Go"),
        Repository(repository_name="repo2", description="Old repo2",
                   visibility="private", gitignore_template="Node", allow_delete=True),
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")

    # Add: repo3 should be added
    assert len(to_add) == 1
    assert to_add[0]["repository_name"] == "repo3"

    # Update: repo1 should be updated
    assert len(to_update) == 1
    assert to_update[0]["repository_name"] == "repo1"
    assert to_update[0]["description"] == "New repo1"

    # Delete: repo2 should be marked for deletion due to allow_delete
    assert len(to_delete) == 1
    assert to_delete[0]["repository_name"] == "repo2"


def test_calculate_diff_no_action():
    """
    Test the calculate_diff function with no action required.
    """
    existing = [
        {"repository_name": "repo1", "description": "Old repo1",
         "visibility": "public", "gitignore_template": "Python"},
    ]
    requested = [
        Repository(repository_name="repo1", description="Old repo1",
                   visibility="public", gitignore_template="Python"),
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")
    assert len(to_add) == 0
    assert len(to_update) == 0
    assert len(to_delete) == 0


def test_calculate_diff_no_delete_without_allow_delete():
    """
    Verify that no delete action occurs when allow_delete is not set to True.
    """
    existing = [
        {"repository_name": "repo1", "description": "Existing repo1",
         "visibility": "public", "gitignore_template": "Python"},
        {"repository_name": "repo2", "description": "Existing repo2",
         "visibility": "private", "gitignore_template": "Node"},
    ]
    requested = [
        Repository(repository_name="repo1", description="Existing repo1",
                   visibility="public", gitignore_template="Python"),
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")
    assert len(to_add) == 0
    assert len(to_update) == 0
    assert len(to_delete) == 0


def test_calculate_diff_with_only_updates():
    """
    Verify that a repository is marked for update if attributes differ.
    """
    existing = [
        {"repository_name": "repo1", "description": "Old repo1",
         "visibility": "public", "gitignore_template": "Python"},
    ]
    requested = [
        Repository(repository_name="repo1", description="Updated repo1",
                   visibility="private", gitignore_template="Python"),
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")
    assert len(to_add) == 0
    assert len(to_update) == 1
    assert len(to_delete) == 0
    assert to_update[0]["repository_name"] == "repo1"
    assert to_update[0]["description"] == "Updated repo1"


def test_calculate_diff_explicit_delete():
    """
    Verify that a repository is marked for deletion if allow_delete is True.
    """
    existing = [
        {"repository_name": "repo1", "description": "Old repo1",
         "visibility": "public", "gitignore_template": "Python"},
    ]
    requested = [
        Repository(repository_name="repo1", description="Old repo1",
                   visibility="public", gitignore_template="Python", allow_delete=True),
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")
    assert len(to_add) == 0
    assert len(to_update) == 0
    assert len(to_delete) == 1
    assert to_delete[0]["repository_name"] == "repo1"


def test_calculate_diff_keyerror():
    """
    Test that a KeyError is raised if an expected key is missing in existing resources.
    """
    existing = [
        {"wrong_key": "repo1", "description": "Repo description",
         "visibility": "public", "gitignore_template": "Python"}
    ]
    requested = [
        Repository(repository_name="repo1", description="Repo description",
                   visibility="public", gitignore_template="Python")
    ]
    with pytest.raises(KeyError) as excinfo:
        calculate_diff(existing, requested, "repository_name")
    assert "Missing required key 'repository_name'" in str(excinfo.value)


class Dummy:
    """Dummy class that only implements model_dump, but not the attribute."""

    def model_dump(self):
        return {"repository_name": "repo1", "description": "Repo description",
                "visibility": "public", "gitignore_template": "Python"}


def test_calculate_diff_attribute_error():
    """
    Test that an AttributeError is raised if a requested resource lacks the unique attribute.
    """
    existing = [
        {"repository_name": "repo1", "description": "Repo description",
         "visibility": "public", "gitignore_template": "Python"}
    ]
    requested = [Dummy()]  # Dummy does not have attribute 'repository_name'
    with pytest.raises(AttributeError) as excinfo:
        calculate_diff(existing, requested, "repository_name")
    assert "Missing required attribute 'repository_name'" in str(excinfo.value)
