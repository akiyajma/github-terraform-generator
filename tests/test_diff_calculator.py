from models.repository import Repository
from utils.diff_calculator import calculate_diff


def test_calculate_diff_add_update_delete():
    """
    Test the calculate_diff function with add, update, and delete cases.

    Test Cases:
    1. Verify that a repository present in 'requested' but not in 'existing' (e.g., with a new `description`
       or `gitignore_template`) is correctly identified as to be added.
    2. Verify that a repository present in both 'existing' and 'requested' but with different attributes 
       (e.g., `description`, `visibility`) is correctly identified as to be updated.
    3. Verify that a repository present in 'existing' but marked with `allow_delete=True` in 'requested' 
       is correctly identified as to be deleted.
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

    # Add
    assert len(to_add) == 1
    assert to_add[0]["repository_name"] == "repo3"

    # Update
    assert len(to_update) == 1
    assert to_update[0]["repository_name"] == "repo1"
    assert to_update[0]["description"] == "New repo1"

    # Delete
    assert len(to_delete) == 1
    assert to_delete[0]["repository_name"] == "repo2"


def test_calculate_diff_no_action():
    """
    Test the calculate_diff function with no action required.

    Test Cases:
    1. Verify that no repositories are added, updated, or deleted when the requested state matches the 
       existing state exactly, including attributes like `description` and `gitignore_template`.
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
    Test the calculate_diff function to ensure no delete action occurs when `allow_delete` is False or not set.

    Test Cases:
    1. Verify that a repository present in 'existing' but not in 'requested' is not marked for deletion 
       unless `allow_delete=True` is explicitly set in 'requested'.
    2. Ensure attributes like `description` and `gitignore_template` are irrelevant when considering deletion.
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
    Test the calculate_diff function to verify updates.

    Test Cases:
    1. Verify that a repository is marked for update if attributes like `description`, `visibility`, 
       or `gitignore_template` differ between 'existing' and 'requested'.
    2. Ensure no repositories are added or deleted if they exist in both states with different attributes.
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
    Test the calculate_diff function to verify explicit delete action.

    Test Cases:
    1. Verify that a repository is marked for deletion if `allow_delete=True` is set in 'requested', even 
       if other attributes like `description` or `gitignore_template` remain unchanged.
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
