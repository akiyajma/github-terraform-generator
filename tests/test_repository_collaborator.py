import os

import pytest
from pydantic import ValidationError

from models.repository_collaborator import RepositoryCollaborator
from utils.tfstate_loader import extract_resources


# ① RepositoryCollaborator モデルのテスト
def test_repository_collaborator_model_valid():
    data = {
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "push"
    }
    collab = RepositoryCollaborator(**data)
    assert collab.repository_name == "repo1"
    assert collab.username == "external_user"
    assert collab.permission == "push"
    # allow_delete のデフォルトは False で、collaborator_id が連結されることを確認
    assert collab.allow_delete is False
    assert collab.collaborator_id == "repo1_external_user"


def test_repository_collaborator_model_invalid_permission():
    data = {
        "repository_name": "repo1",
        "username": "external_user",
        "permission": "invalid"  # 不正な permission を指定
    }
    with pytest.raises(ValidationError):
        RepositoryCollaborator(**data)

# ② Jinja2 テンプレートを用いた Terraform ファイル生成のテスト


@pytest.fixture
def temp_template_dir(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    # repository_collaborator.tf.j2 テンプレートを用意
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
    output_dir = tmp_path / "terraform"
    output_dir.mkdir()
    return str(output_dir)


def test_generate_repository_collaborator(temp_template_dir, temp_output_dir):
    from generator.repository_collaborator_generator import (
        generate_repository_collaborator,
    )
    from models.repository_collaborator import RepositoryCollaborator
    collab = RepositoryCollaborator(
        repository_name="repo1",
        username="external_user",
        permission="push"
    )
    generate_repository_collaborator(
        collab, temp_template_dir, temp_output_dir)
    # 出力ファイルの名前は "username_repositoryname_collaborator.tf" となる（例: external_user_repo1_collaborator.tf）
    output_file = os.path.join(
        temp_output_dir, "external_user_repo1_collaborator.tf")
    assert os.path.exists(output_file)
    content = open(output_file).read()
    assert 'resource "github_repository_collaborator" "external_user"' in content
    assert 'repository = "repo1"' in content
    assert 'username   = "external_user"' in content
    assert 'permission = "push"' in content

# ③ tfstate からの抽出テスト（repository collaborator の抽出）


def test_extract_resources_repository_collaborator():
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

# ④ process_repo_collaborators の例外処理などのテスト


def test_process_repo_collaborators_add_exception(tmp_path):
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
    from unittest.mock import MagicMock

    from utils.process_resources import process_repo_collaborators
    dummy_generator = MagicMock()
    dummy_generator.generate_repository_collaborator.side_effect = None

    # 出力先にあらかじめ削除対象となるファイルを作成しておく
    output_dir = str(tmp_path)
    file_path = os.path.join(output_dir, "external_user_repo1_collaborator.tf")
    with open(file_path, "w") as f:
        f.write("dummy")
    # 削除処理をテストするため、更新・追加は空リストとする
    # ※ process_repo_collaborators 内で削除対象も処理するので、存在すれば削除される
    process_repo_collaborators(dummy_generator, output_dir, [], [], [
                               {"repository_name": "repo1", "username": "external_user", "permission": "push"}])
    assert not os.path.exists(file_path)
