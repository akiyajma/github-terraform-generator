import os

import pytest

from generator.repository_generator import generate_repository
from generator.team_generator import generate_team
from models.repository import Repository
from models.team import Team


@pytest.fixture
def temp_output_dir(tmpdir):
    """
    Fixture to create a temporary output directory for testing.
    """
    return tmpdir.mkdir("output")


def test_generate_repository(temp_output_dir):
    """
    Test the generate_repository function to ensure it generates the Terraform file.

    Test Cases:
    1. Verify that the Terraform file is created in the output directory.
    2. Verify that the content of the generated Terraform file includes the repository resource.
    """
    repo = Repository(
        repository_name="test-repo",
        description="Test repository",
        visibility="public",
        gitignore_template="Python"
    )
    template_dir = "templates"
    output_dir = str(temp_output_dir)
    generate_repository(repo, template_dir, output_dir)

    generated_file = os.path.join(output_dir, "test-repo_repository.tf")
    assert os.path.exists(generated_file)
    with open(generated_file, "r") as f:
        content = f.read()
        assert 'resource "github_repository" "test-repo"' in content
        assert 'gitignore_template = "Python"' in content


def test_generate_team(temp_output_dir):
    """
    Test the generate_team function to ensure it generates the Terraform file correctly.

    Test Cases:
    1. Verify that the Terraform file is created in the output directory.
    2. Verify that the content of the generated Terraform file includes the team resource.
    """
    team = Team(
        team_name="test-team",
        description="Test team",
        privacy="closed",
        members=[
            {"username": "user1", "role": "maintainer"},
            {"username": "user2", "role": "member"},
            {"username": "user3", "role": "member"}
        ],
    )
    template_dir = "templates"
    output_dir = str(temp_output_dir)
    generate_team(team, template_dir, output_dir)

    generated_file = os.path.join(output_dir, "test-team_team.tf")
    assert os.path.exists(generated_file)
    with open(generated_file, "r") as f:
        content = f.read()
        assert 'resource "github_team" "test-team"' in content
