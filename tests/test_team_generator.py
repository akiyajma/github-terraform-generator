from unittest.mock import patch

import pytest

from generator.team_generator import generate_team
from models import Team


@pytest.fixture
def team_dict():
    return {
        "team_name": "dev-team",
        "description": "Development team",
        "privacy": "closed",
        "members": [
            {"username": "dev.user@example.com", "role": "maintainer"},
            {"username": "john.doe@domain.com", "role": "member"}
        ]
    }


@pytest.fixture
def team_obj():
    return Team(
        team_name="dev-team",
        description="Development team",
        privacy="closed",
        members=[
            {"username": "dev.user@example.com", "role": "maintainer"},
            {"username": "john.doe@domain.com", "role": "member"}
        ]
    )


def test_generate_team_with_dict(team_dict, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "team.tf.j2").write_text(
        "{{ team_name }} {{ description }} {{ privacy }} {% for member in members %}{{ member.username.split('@')[0] }} {{ member.role }} {% endfor %}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_team(team_dict, str(template_dir), str(output_dir))

    output_file = output_dir / "dev-team_team.tf"
    assert output_file.read_text(
    ) == "dev-team Development team closed dev.user maintainer john.doe member "


def test_generate_team_with_obj(team_obj, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "team.tf.j2").write_text(
        "{{ team_name }} {{ description }} {{ privacy }} {% for member in members %}{{ member.username.split('@')[0] }} {{ member.role }} {% endfor %}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_team(team_obj, str(template_dir), str(output_dir))

    output_file = output_dir / "dev-team_team.tf"
    assert output_file.read_text(
    ) == "dev-team Development team closed dev.user maintainer john.doe member "


def test_generate_team_invalid_data(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "team.tf.j2").write_text(
        "{{ team_name }} {{ description }} {{ privacy }} {% for member in members %}{{ member.username.split('@')[0] }} {{ member.role }} {% endfor %}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(Exception, match="Error generating Terraform file for team:"):
        generate_team({}, str(template_dir), str(output_dir))


@patch("generator.team_generator._write_to_file")
def test_generate_team_template_not_found(mock_write, team_dict, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(Exception, match="Error generating Terraform file for team:"):
        generate_team(team_dict, str(template_dir), str(output_dir))
