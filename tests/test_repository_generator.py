from unittest.mock import patch

import pytest

from generator.repository_generator import generate_repository
from models import Repository


@pytest.fixture
def repository_dict():
    return {
        "repository_name": "example-repo",
        "description": "An example repository",
        "visibility": "public",
        "gitignore_template": "Python"
    }


@pytest.fixture
def repository_obj():
    return Repository(
        repository_name="example-repo",
        description="An example repository",
        visibility="public",
        gitignore_template="Python"
    )


def test_generate_repository_with_dict(repository_dict, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "repository.tf.j2").write_text(
        "{{ repository_name }} {{ description }} {{ visibility }} {{ gitignore_template }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_repository(repository_dict, str(template_dir), str(output_dir))

    output_file = output_dir / "example-repo_repository.tf"
    assert output_file.read_text() == "example-repo An example repository public Python"


def test_generate_repository_with_obj(repository_obj, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "repository.tf.j2").write_text(
        "{{ repository_name }} {{ description }} {{ visibility }} {{ gitignore_template }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_repository(repository_obj, str(template_dir), str(output_dir))

    output_file = output_dir / "example-repo_repository.tf"
    assert output_file.read_text() == "example-repo An example repository public Python"


def test_generate_repository_gitignore_none(repository_dict, tmp_path):
    repository_dict["gitignore_template"] = "None"
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "repository.tf.j2").write_text(
        "{{ repository_name }} {{ description }} {{ visibility }} {% if gitignore_template != 'None' %}{{ gitignore_template }}{% endif %}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_repository(repository_dict, str(template_dir), str(output_dir))

    output_file = output_dir / "example-repo_repository.tf"
    assert output_file.read_text() == "example-repo An example repository public "


def test_generate_repository_invalid_data(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "repository.tf.j2").write_text(
        "{{ repository_name }} {{ description }} {{ visibility }} {{ gitignore_template }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(Exception, match="Error generating Terraform file for repository:"):
        generate_repository({}, str(template_dir), str(output_dir))


@patch("generator.repository_generator._write_to_file")
def test_generate_repository_template_not_found(mock_write, repository_dict, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(Exception, match="Error generating Terraform file for repository:"):
        generate_repository(repository_dict, str(
            template_dir), str(output_dir))
