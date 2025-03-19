import os

import pytest

from generator.terraform_generator import TerraformGenerator
from models.membership import Membership
from models.repository import Repository
from models.team import Team


@pytest.fixture
def temp_template_dir(tmp_path):
    """
    一時テンプレートディレクトリを作成し、必要な Jinja2 テンプレートファイルを用意する。
    """
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    # repository.tf.j2 テンプレート
    (template_dir / "repository.tf.j2").write_text(
        'resource "github_repository" "{{ repository_name }}" {\n'
        '  description = "{{ description }}"\n'
        '  visibility  = "{{ visibility }}"\n'
        '{% if gitignore_template and gitignore_template != "None" %}  gitignore_template = "{{ gitignore_template }}"\n{% endif %}'
        '}\n'
    )
    # team.tf.j2 テンプレート
    (template_dir / "team.tf.j2").write_text(
        'resource "github_team" "{{ team_name }}" {\n'
        '  description = "{{ description }}"\n'
        '  privacy     = "{{ privacy }}"\n'
        '}\n'
    )
    # membership.tf.j2 テンプレート
    (template_dir / "membership.tf.j2").write_text(
        'resource "github_membership" "{{ membership.username }}" {\n'
        '  role = "{{ membership.role }}"\n'
        '}\n'
    )
    return str(template_dir)


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    一時出力ディレクトリを作成する。
    """
    output_dir = tmp_path / "terraform"
    output_dir.mkdir()
    return str(output_dir)


def test_generate_repository_single(temp_template_dir, temp_output_dir):
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
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    repo_list = [
        Repository(
            repository_name="repo1",
            description="Test repository",
            visibility="public",
            gitignore_template="Python"
        ),
        Repository(
            repository_name="repo2",
            description="Second repository",
            visibility="private",
            gitignore_template="None"
        )
    ]
    tg.generate_repository(repo_list)
    output_file1 = os.path.join(temp_output_dir, "repo1_repository.tf")
    output_file2 = os.path.join(temp_output_dir, "repo2_repository.tf")
    assert os.path.exists(output_file1)
    assert os.path.exists(output_file2)


def test_generate_team_single(temp_template_dir, temp_output_dir):
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
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    # 無効なチームデータ（必須項目が不足）を渡すと ValueError が発生する
    with pytest.raises(ValueError):
        tg.generate_team({})


def test_generate_membership_single(temp_template_dir, temp_output_dir):
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    membership = Membership(username="user1", role="member")
    tg.generate_membership(membership)
    output_file = os.path.join(temp_output_dir, "user1_membership.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_membership" "user1"' in content
    assert 'role = "member"' in content


def test_generate_membership_list(temp_template_dir, temp_output_dir):
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    memberships = [
        Membership(username="user1", role="member"),
        Membership(username="user2", role="admin")
    ]
    tg.generate_membership(memberships)
    output_file1 = os.path.join(temp_output_dir, "user1_membership.tf")
    output_file2 = os.path.join(temp_output_dir, "user2_membership.tf")
    assert os.path.exists(output_file1)
    assert os.path.exists(output_file2)


def test_generate_membership_invalid(temp_template_dir, temp_output_dir):
    tg = TerraformGenerator(temp_template_dir, temp_output_dir)
    # 無効な membership データ（辞書として必須キーが不足）を渡すと例外が発生する
    with pytest.raises(Exception):
        tg.generate_membership({})
