import pytest

from models.repository import Repository
from utils.diff_calculator import calculate_diff


def test_calculate_diff_add_update_delete():
    """
    Test `calculate_diff` function for handling additions, updates, and deletions.

    This test ensures that:
    - A new repository (`repo3`) is correctly added.
    - An existing repository (`repo1`) with modified attributes is updated.
    - A repository (`repo2`) marked with `allow_delete=True` is scheduled for deletion.

    Steps:
    1. Define an `existing` list with repositories currently in the state.
    2. Define a `requested` list with the desired repositories, including:
       - `repo1` (modified)
       - `repo2` (marked for deletion)
       - `repo3` (new addition)
    3. Execute `calculate_diff()`.
    4. Validate that:
       - `to_add` contains `repo3`.
       - `to_update` contains `repo1` with the updated attributes.
       - `to_delete` contains `repo2`.

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

    assert len(to_add) == 1
    assert to_add[0]["repository_name"] == "repo3"

    assert len(to_update) == 1
    assert to_update[0]["repository_name"] == "repo1"
    assert to_update[0]["description"] == "New repo1"

    assert len(to_delete) == 1
    assert to_delete[0]["repository_name"] == "repo2"


def test_calculate_diff_no_action():
    """
    Test `calculate_diff` when no changes are required.

    This test ensures that if the existing and requested states are identical,
    the function does not produce any additions, updates, or deletions.

    Steps:
    1. Define identical `existing` and `requested` lists.
    2. Execute `calculate_diff()`.
    3. Verify that `to_add`, `to_update`, and `to_delete` are all empty.
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
    Ensure `calculate_diff` does not delete a repository unless explicitly marked.

    Steps:
    1. Define an `existing` state with multiple repositories.
    2. Define a `requested` state with fewer repositories but without `allow_delete=True`.
    3. Execute `calculate_diff()`.
    4. Ensure that no deletions are scheduled (`to_delete` is empty).
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
    Verify `calculate_diff` correctly detects updates when no additions or deletions exist.

    Steps:
    1. Define `existing` and `requested` repositories, where the requested one has modified attributes.
    2. Execute `calculate_diff()`.
    3. Ensure `to_update` contains the modified repository, while `to_add` and `to_delete` remain empty.
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
    Ensure a repository is marked for deletion only when `allow_delete=True`.

    Steps:
    1. Define an `existing` repository.
    2. Define a `requested` repository with `allow_delete=True`.
    3. Execute `calculate_diff()`.
    4. Verify the repository is added to `to_delete`.
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
    Ensure `calculate_diff` raises a KeyError when an expected key is missing.

    Steps:
    1. Define an `existing` repository with an incorrect key (`wrong_key` instead of `repository_name`).
    2. Define a valid `requested` repository.
    3. Execute `calculate_diff()` and expect a `KeyError`.
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
    """Dummy class that only implements `model_dump`, but not the required attribute."""

    def model_dump(self):
        return {"repository_name": "repo1", "description": "Repo description",
                "visibility": "public", "gitignore_template": "Python"}


def test_calculate_diff_attribute_error():
    """
    Ensure `calculate_diff` raises an AttributeError when a requested resource lacks the unique key.

    Steps:
    1. Define an `existing` repository with valid attributes.
    2. Define a `requested` repository using a `Dummy` class that lacks the required `repository_name` attribute.
    3. Execute `calculate_diff()` and expect an `AttributeError`.
    """
    existing = [
        {"repository_name": "repo1", "description": "Repo description",
         "visibility": "public", "gitignore_template": "Python"}
    ]
    requested = [Dummy()]  # Dummy does not have attribute 'repository_name'
    with pytest.raises(AttributeError) as excinfo:
        calculate_diff(existing, requested, "repository_name")
    assert "Missing required attribute 'repository_name'" in str(excinfo.value)
