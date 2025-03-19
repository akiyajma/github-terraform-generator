import os

import pytest

from generator.terraform_generator import TerraformGenerator
from models.membership import Membership
from models.repository import Repository
from models.team import Team


@pytest.fixture
def temp_template_dir(tmp_path):
    """
    Create a temporary directory for storing Jinja2 template files.

    This fixture generates a `templates` directory and populates it with necessary
    Jinja2 template files used for generating Terraform configurations.

    Returns:
        str: The path to the temporary template directory.
    """
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    # Template for GitHub repository
    (template_dir / "repository.tf.j2").write_text(
        'resource "github_repository" "{{ repository_name }}" {\n'
        '  description = "{{ description }}"\n'
        '  visibility  = "{{ visibility }}"\n'
        '{% if gitignore_template and gitignore_template != "None" %}  gitignore_template = "{{ gitignore_template }}"\n{% endif %}'
        '}\n'
    )

    # Template for GitHub team
    (template_dir / "team.tf.j2").write_text(
        'resource "github_team" "{{ team_name }}" {\n'
        '  description = "{{ description }}"\n'
        '  privacy     = "{{ privacy }}"\n'
        '}\n'
    )

    # Template for GitHub membership
    (template_dir / "membership.tf.j2").write_text(
        'resource "github_membership" "{{ membership.username }}" {\n'
        '  role = "{{ membership.role }}"\n'
        '}\n'
    )

    # Template for GitHub repository collaborators
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
    Create a temporary directory for storing Terraform output files.

    Returns:
        str: The path to the temporary output directory.
    """
    output_dir = tmp_path / "terraform"
    output_dir.mkdir()
    return str(output_dir)


def test_generate_repository_single(temp_template_dir, temp_output_dir):
    """
    Test generating a single GitHub repository Terraform configuration.

    This test ensures that a single repository configuration file is created correctly.

    Steps:
    1. Create a `Repository` object.
    2. Invoke `generate_repository()` method.
    3. Verify that the Terraform file is created with correct content.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    repo = Repository(
        repository_name="repo1",
        description="Test repository",
        visibility="public",
        gitignore_template="Python"
    )
    tg.generate_repository(repo)
    output_file = os.path.join(temp_output_dir, "repo1_repository.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_repository" "repo1"' in content
    assert 'gitignore_template = "Python"' in content


def test_generate_repository_list(temp_template_dir, temp_output_dir):
    """
    Test generating multiple GitHub repositories.

    This test verifies that multiple repository Terraform files are generated correctly.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    repo_list = [
        Repository(repository_name="repo1", description="Test repository",
                   visibility="public", gitignore_template="Python"),
        Repository(repository_name="repo2", description="Second repository",
                   visibility="private", gitignore_template="None")
    ]
    tg.generate_repository(repo_list)
    assert os.path.exists(os.path.join(temp_output_dir, "repo1_repository.tf"))
    assert os.path.exists(os.path.join(temp_output_dir, "repo2_repository.tf"))


def test_generate_team_single(temp_template_dir, temp_output_dir):
    """
    Test generating a single GitHub team Terraform configuration.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    team = Team(
        team_name="team1",
        description="Test team",
        privacy="closed",
        members=[{"username": "user1", "role": "maintainer"}]
    )
    tg.generate_team(team)
    output_file = os.path.join(temp_output_dir, "team1_team.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_team" "team1"' in content


def test_generate_team_invalid(temp_template_dir, temp_output_dir):
    """
    Test generating a GitHub team with invalid data.

    This test ensures that attempting to generate a team without required attributes
    raises a `ValueError`.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    with pytest.raises(ValueError):
        tg.generate_team({})


def test_generate_membership_single(temp_template_dir, temp_output_dir):
    """
    Test generating a single GitHub membership Terraform configuration.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    membership = Membership(username="user1", role="member")
    tg.generate_membership(membership)
    output_file = os.path.join(temp_output_dir, "user1_membership.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_membership" "user1"' in content
    assert 'role = "member"' in content


def test_generate_membership_list(temp_template_dir, temp_output_dir):
    """
    Test generating multiple GitHub memberships.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    memberships = [
        Membership(username="user1", role="member"),
        Membership(username="user2", role="admin")
    ]
    tg.generate_membership(memberships)
    assert os.path.exists(os.path.join(temp_output_dir, "user1_membership.tf"))
    assert os.path.exists(os.path.join(temp_output_dir, "user2_membership.tf"))


def test_generate_membership_invalid(temp_template_dir, temp_output_dir):
    """
    Test generating a GitHub membership with invalid data.

    This test ensures that an exception is raised when required attributes are missing.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    with pytest.raises(Exception):
        tg.generate_membership({})


def test_generate_repository_collaborator_single(temp_template_dir, temp_output_dir):
    """
    Test generating a single GitHub repository collaborator Terraform configuration.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    collab_data = {
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "push"
    }
    tg.generate_repository_collaborator(collab_data)
    output_file = os.path.join(
        temp_output_dir, "external_user_repo1_collaborator.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_repository_collaborator" "external_user"' in content
    assert 'repository = "repo1"' in content
    assert 'username   = "external_user"' in content
    assert 'permission = "push"' in content


def test_generate_repository_collaborator_list(temp_template_dir, temp_output_dir):
    """
    Test generating multiple GitHub repository collaborators.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    collab_list = [
        {"repository_name": "repo1", "username": "external_user", "permission": "push"},
        {"repository_name": "repo2", "username": "external_user2", "permission": "pull"}
    ]
    tg.generate_repository_collaborator(collab_list)
    assert os.path.exists(os.path.join(
        temp_output_dir, "external_user_repo1_collaborator.tf"))
    assert os.path.exists(os.path.join(
        temp_output_dir, "external_user2_repo2_collaborator.tf"))


def test_generate_repository_collaborator_invalid(temp_template_dir, temp_output_dir):
    """
    Test generating a GitHub repository collaborator with missing required attributes.

    This test ensures that an exception is raised when required attributes such as
    `repository_name` are missing.
    """
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    with pytest.raises(Exception):
        tg.generate_repository_collaborator(
            {"username": "external_user", "permission": "push"})
