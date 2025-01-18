from models.repository import Repository
from utils.diff_calculator import calculate_diff


def test_calculate_diff():
    """
    Test the calculate_diff function.

    Test Cases:
    1. Verify that a repository present in 'requested' but not in 'existing' is added.
    2. Verify that a repository present in both 'existing' and 'requested' but with different attributes is updated.
    3. Verify that a repository present in 'existing' but not in 'requested' is deleted.
    """
    existing = [
        {"repository_name": "repo1", "visibility": "public",
            "gitignore_template": "Python"},
        {"repository_name": "repo2", "visibility": "private",
            "gitignore_template": "Node"}
    ]
    requested = [
        Repository(repository_name="repo1", description="",
                   visibility="private", gitignore_template="Python"),
        Repository(repository_name="repo3", description="",
                   visibility="public", gitignore_template="Go")
    ]

    to_add, to_update, to_delete = calculate_diff(
        existing, requested, "repository_name")

    assert len(to_add) == 1
    assert to_add[0]["repository_name"] == "repo3"

    assert len(to_update) == 1
    assert to_update[0]["repository_name"] == "repo1"

    assert len(to_delete) == 1
    assert to_delete[0]["repository_name"] == "repo2"
