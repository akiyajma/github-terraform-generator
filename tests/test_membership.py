import os

import pytest
from pydantic import ValidationError

from generator.membership_generator import generate_membership
from models.membership import Membership


@pytest.fixture
def temp_template_dir(tmp_path):
    """
    Create a temporary template directory and add a `membership.tf.j2` template file.

    This fixture generates a `templates` directory and writes a basic Jinja2 template
    file for GitHub membership, which includes placeholders for `username`, `role`, and `action`.

    Returns:
        str: The path to the temporary template directory.
    """
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template_file = templates_dir / "membership.tf.j2"

    # A simple Jinja2 template for rendering membership attributes
    template_file.write_text(
        'resource "github_membership" "{{ membership.username }}" {\n'
        '  role = "{{ membership.role }}"\n'
        '  action = "{{ action }}"\n'
        '}\n'
    )
    return str(templates_dir)


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


@pytest.fixture(autouse=True)
def cleanup_generated_file(temp_output_dir):
    """
    Automatically clean up the generated membership Terraform file after each test.

    This fixture ensures that any generated `user1_membership.tf` file is removed after
    the test completes.

    Yields:
        None
    """
    yield
    membership_file = os.path.join(temp_output_dir, "user1_membership.tf")
    if os.path.exists(membership_file):
        os.remove(membership_file)


def test_membership_model_valid():
    """
    Test that a valid `Membership` model is successfully created.

    This test verifies that:
    - The `username` and `role` attributes are correctly assigned.
    - The default value of `allow_delete` is `False`.
    """
    membership = Membership(username="user1", role="member")
    assert membership.username == "user1"
    assert membership.role == "member"
    assert membership.allow_delete is False


def test_membership_model_invalid_role():
    """
    Test that `ValidationError` is raised for an invalid `role` value.

    This test ensures that attempting to create a `Membership` instance with
    an invalid role (not `member` or `admin`) raises a `ValidationError`.
    """
    with pytest.raises(ValidationError):
        Membership(username="user1", role="invalid")


def test_generate_membership_valid(temp_template_dir, temp_output_dir):
    """
    Test generating a valid Terraform file for a GitHub membership.

    This test verifies that:
    - A Terraform file is created successfully.
    - The rendered file correctly contains the membership details (`username`, `role`).
    - The specified `action` is correctly included in the output.

    Steps:
    1. Create a `Membership` object with valid attributes.
    2. Call `generate_membership()` with `action="create"`.
    3. Verify that the Terraform file is created.
    4. Check the file content to ensure proper rendering.
    """
    membership = Membership(username="user1", role="member")
    generate_membership(membership, temp_template_dir,
                        temp_output_dir, action="create")

    output_file = os.path.join(temp_output_dir, "user1_membership.tf")
    assert os.path.exists(output_file)

    with open(output_file, "r") as f:
        content = f.read()

    assert 'resource "github_membership" "user1"' in content
    assert 'role = "member"' in content
    assert 'action = "create"' in content


def test_generate_membership_invalid_action(temp_template_dir, temp_output_dir):
    """
    Test that `ValueError` is raised when an invalid `action` is provided.

    This test ensures that calling `generate_membership()` with an unsupported `action`
    (not `create`, `update`, or `delete`) results in a `ValueError`.
    """
    membership = Membership(username="user1", role="member")
    with pytest.raises(ValueError):
        generate_membership(membership, temp_template_dir,
                            temp_output_dir, action="invalid")
