import os

import pytest
from pydantic import ValidationError

from models.repository_collaborator import RepositoryCollaborator
from utils.tfstate_loader import extract_resources

# --- Tests for RepositoryCollaborator model ---


def test_repository_collaborator_model_valid():
    """
    Test that a valid `RepositoryCollaborator` model is created successfully.

    This test ensures that:
    - The model correctly initializes with the provided attributes.
    - The `collaborator_id` is correctly constructed as "<repository_name>_<username>".
    - The default value of `allow_delete` is `False`.
    """
    data = {
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "push"
    }
    collab = RepositoryCollaborator(**data)
    assert collab.repository_name == "repo1"
    assert collab.username == "external_user"
    assert collab.permission == "push"
    assert collab.allow_delete is False
    assert collab.collaborator_id == "repo1_external_user"


def test_repository_collaborator_model_invalid_permission():
    """
    Test that a `ValidationError` is raised for an invalid `permission` value.

    This test verifies that providing an unsupported `permission` value
    (not "pull", "push", or "admin") triggers a validation error.
    """
    data = {
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "invalid"
    }
    with pytest.raises(ValidationError):
        RepositoryCollaborator(**data)


# --- Tests for Terraform file generation using Jinja2 templates ---


@pytest.fixture
def temp_template_dir(tmp_path):
    """
    Create a temporary template directory containing a `repository_collaborator.tf.j2` template.

    The template is used for generating Terraform files related to GitHub repository collaborators.

    Returns:
        str: The path to the temporary template directory.
    """
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "repository_collaborator.tf.j2").write_text(
        'resource "github_repository_collaborator" "{{ repository_collaborator.username }}" {\n'
        '  repository = "{{ repository_collaborator.repository_name }}"\n'
        '  username   = "{{ repository_collaborator.username }}"\n'
        '  permission = "{{ repository_collaborator.permission }}"\n'
        '}\n'
    )
    return str(template_dir)


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Create a temporary output directory for storing generated Terraform files.

    Returns:
        str: The path to the temporary output directory.
    """
    output_dir = tmp_path / "terraform"
    output_dir.mkdir()
    return str(output_dir)


def test_generate_repository_collaborator(temp_template_dir, temp_output_dir):
    """
    Test that `generate_repository_collaborator` correctly generates a Terraform file.

    This test ensures that:
    - The output file is created with the correct naming format.
    - The contents of the file correctly render the collaborator's attributes.
    """
    from generator.repository_collaborator_generator import (
        generate_repository_collaborator,
    )

    collab = RepositoryCollaborator(
        repository_name="repo1",
        username="external_user",
        permission="push"
    )
    generate_repository_collaborator(
        collab, temp_template_dir, temp_output_dir)

    output_file = os.path.join(
        temp_output_dir, "external_user_repo1_collaborator.tf")
    assert os.path.exists(output_file)

    with open(output_file, "r") as f:
        content = f.read()

    assert 'resource "github_repository_collaborator" "external_user"' in content
    assert 'repository = "repo1"' in content
    assert 'username   = "external_user"' in content
    assert 'permission = "push"' in content


# --- Tests for extracting repository collaborators from Terraform state ---


def test_extract_resources_repository_collaborator():
    """
    Test that `extract_resources` correctly extracts repository collaborators from a Terraform state file.

    This test ensures that:
    - The extracted data contains the correct repository collaborator attributes.
    - The extracted collaborator's `collaborator_id` is correctly formatted.
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository_collaborator",
                "instances": [
                    {
                        "attributes": {
                            "repository": "repo1",
                            "username": "external_user",
                            "permission": "push"
                        }
                    }
                ]
            }
        ]
    }
    result = extract_resources(tfstate)
    assert "repository_collaborators" in result
    assert len(result["repository_collaborators"]) == 1
    collab = result["repository_collaborators"][0]
    assert collab["repository_name"] == "repo1"
    assert collab["username"] == "external_user"
    assert collab["permission"] == "push"
    assert collab["collaborator_id"] == "repo1_external_user"


# --- Tests for processing repository collaborators ---


def test_process_repo_collaborators_add_exception(tmp_path):
    """
    Ensure `process_repo_collaborators` raises an exception when adding a collaborator fails.

    This test mocks an error when calling `generate_repository_collaborator` for an addition,
    ensuring that an appropriate exception is raised.
    """
    from unittest.mock import MagicMock

    from utils.process_resources import process_repo_collaborators

    dummy_generator = MagicMock()
    dummy_generator.generate_repository_collaborator.side_effect = Exception(
        "Collaborator add error")

    collaborators_to_add = [{
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "push"
    }]

    with pytest.raises(Exception) as excinfo:
        process_repo_collaborators(dummy_generator, str(
            tmp_path), collaborators_to_add, [], [])
    assert "Error adding repository collaborator" in str(excinfo.value)


def test_process_repo_collaborators_success(tmp_path):
    """
    Ensure `process_repo_collaborators` correctly deletes existing Terraform files for removed collaborators.

    This test:
    - Creates a Terraform file for a repository collaborator.
    - Runs `process_repo_collaborators` with a deletion request.
    - Confirms that the file is properly removed.
    """
    from unittest.mock import MagicMock

    from utils.process_resources import process_repo_collaborators

    dummy_generator = MagicMock()
    dummy_generator.generate_repository_collaborator.side_effect = None

    output_dir = str(tmp_path)
    file_path = os.path.join(output_dir, "external_user_repo1_collaborator.tf")

    with open(file_path, "w") as f:
        f.write("dummy")

    process_repo_collaborators(dummy_generator, output_dir, [], [], [
        {"repository_name": "repo1", "username": "external_user", "permission": "push"}
    ])

    assert not os.path.exists(file_path)
