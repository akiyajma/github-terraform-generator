import json
import os

import pytest

from utils.tfstate_loader import extract_resources, load_tfstate, save_existing_state


def test_extract_resources_valid():
    """
    Test `extract_resources` function for successful extraction.

    This test verifies that repositories, teams, and memberships are correctly
    extracted from a valid Terraform state (`tfstate`).

    Steps:
    1. Define a `tfstate` with:
       - A repository (`repo1`)
       - A team (`team1`)
       - A membership (`user1`)
    2. Call `extract_resources()`.
    3. Validate that:
       - The repository count is correct, and `repository_name` is extracted properly.
       - The team count is correct, and `team_name` is extracted properly.
       - The membership count is correct, and `username` is extracted properly.
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            "name": "repo1",
                            "description": "Repo description",
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
                            "description": "Team description",
                            "privacy": "closed"
                        }
                    }
                ]
            },
            {
                "type": "github_membership",
                "instances": [
                    {
                        "attributes": {
                            "username": "user1",
                            "role": "member"
                        }
                    }
                ]
            }
        ]
    }
    result = extract_resources(tfstate)
    assert len(result["repositories"]) == 1
    assert result["repositories"][0]["repository_name"] == "repo1"
    assert len(result["teams"]) == 1
    assert result["teams"][0]["team_name"] == "team1"
    assert len(result["memberships"]) == 1
    assert result["memberships"][0]["username"] == "user1"


def test_extract_resources_keyerror():
    """
    Test that `extract_resources` raises a `KeyError` when an expected key is missing.

    This test ensures that:
    - A missing key (`name` in `github_repository`) results in a `KeyError`.
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            # Missing "name" key
                            "description": "No name repo",
                            "visibility": "public",
                            "gitignore_template": "Python"
                        }
                    }
                ]
            }
        ]
    }
    with pytest.raises(KeyError) as excinfo:
        extract_resources(tfstate)
    assert "Missing expected key" in str(excinfo.value)


def test_extract_resources_unexpected_exception():
    """
    Test that `extract_resources` handles unexpected exceptions.

    This test introduces an invalid `instances` value (a string instead of a list)
    to trigger an `AttributeError` in the loop.
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": "not a list"  # Invalid structure
            }
        ]
    }
    with pytest.raises(Exception) as excinfo:
        extract_resources(tfstate)
    assert "Unexpected error extracting resources" in str(excinfo.value)


def test_load_tfstate_file_not_found(tmp_path):
    """
    Test that `load_tfstate` raises `FileNotFoundError` for a missing file.

    This test ensures that attempting to load a non-existent `tfstate` file
    correctly raises an exception.
    """
    non_existent = tmp_path / "nonexistent.tfstate"
    with pytest.raises(FileNotFoundError):
        load_tfstate(str(non_existent))


def test_load_tfstate_invalid_json(tmp_path):
    """
    Test that `load_tfstate` raises `json.JSONDecodeError` for invalid JSON content.

    This test writes an invalid JSON string to a file and ensures that
    `load_tfstate()` raises an error when attempting to parse it.
    """
    file_path = tmp_path / "invalid.tfstate"
    file_path.write_text("not valid json")
    with pytest.raises(json.JSONDecodeError):
        load_tfstate(str(file_path))


def test_load_tfstate_valid(tmp_path):
    """
    Test that `load_tfstate` correctly loads a valid Terraform state file.

    Steps:
    1. Write a valid JSON Terraform state file.
    2. Call `load_tfstate()`.
    3. Ensure that the returned dictionary matches the expected content.
    """
    data = {"resources": []}
    file_path = tmp_path / "valid.tfstate"
    file_path.write_text(json.dumps(data))
    result = load_tfstate(str(file_path))
    assert result == data


def test_save_existing_state(tmp_path):
    """
    Test `save_existing_state` function for correct JSON file generation.

    Steps:
    1. Define a state dictionary with repositories and teams.
    2. Call `save_existing_state()` to save it as a JSON file.
    3. Load the file and verify that the content matches the original state.
    """
    state = {
        "repositories": [{"repository_name": "repo1", "visibility": "public", "description": "A repo"}],
        "teams": [{"team_name": "team1", "description": "A team", "privacy": "closed"}]
    }
    file_path = tmp_path / "existing_state.json"
    save_existing_state(state, str(file_path))
    with open(str(file_path), "r") as f:
        loaded = json.load(f)
    assert loaded == state


def test_save_existing_state_oserror(monkeypatch, tmp_path):
    """
    Test that `save_existing_state` raises an `OSError` if the output directory cannot be created.

    This test patches `os.makedirs` to simulate a failure when creating directories.
    """
    file_path = tmp_path / "existing_state.json"

    # Patch `os.makedirs` to raise an `OSError`
    monkeypatch.setattr(os, "makedirs", lambda path, exist_ok=True: (
        _ for _ in ()).throw(OSError("Test OSError"))
    )

    with pytest.raises(OSError) as excinfo:
        save_existing_state({}, str(file_path))
    assert "Failed to save existing state" in str(excinfo.value)
