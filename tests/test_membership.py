import os
from unittest.mock import MagicMock

import pytest

from utils.process_resources import process_resources


# autouse フィクスチャ: テスト終了後に生成された Terraform ファイルを削除
@pytest.fixture(autouse=True)
def cleanup_generated_files():
    yield  # テスト実行
    # membership の生成ファイル
    membership_path = os.path.join("terraform", "user1_membership.tf")
    if os.path.exists(membership_path):
        os.remove(membership_path)
    # repository の生成ファイル（例: example-repo_repository.tf）
    repo_path = os.path.join("terraform", "example-repo_repository.tf")
    if os.path.exists(repo_path):
        os.remove(repo_path)
    # team の生成ファイル（例: example-team_team.tf）
    team_path = os.path.join("terraform", "example-team_team.tf")
    if os.path.exists(team_path):
        os.remove(team_path)


def test_process_repositories_addition(mocker):
    # TerraformGenerator のインスタンス生成をモックする
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.repos_to_add = [
        {"repository_name": "repo1", "visibility": "public",
            "description": "New repo", "gitignore_template": "Python"}
    ]
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    # teams, memberships は空リストを設定してエラー回避
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_repository.assert_called_once_with(
        resource_changes.repos_to_add[0])


def test_process_repositories_update(mocker):
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = [
        {"repository_name": "repo1", "visibility": "public",
            "description": "Updated repo", "gitignore_template": "Python"}
    ]
    resource_changes.repos_to_delete = []
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_repository.assert_called_once_with(
        resource_changes.repos_to_update[0])


def test_process_repositories_deletion(mocker):
    # 削除の場合は、生成済みのファイルを削除する処理を検証
    output_dir = "terraform"
    os.makedirs(output_dir, exist_ok=True)
    tf_file = os.path.join(output_dir, "repo1_repository.tf")
    with open(tf_file, "w") as f:
        f.write("dummy")

    resource_changes = MagicMock()
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = [{"repository_name": "repo1"}]
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    # TerraformGenerator の生成は不要なためモックで置換
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=MagicMock())
    process_resources("templates", output_dir, resource_changes)

    assert not os.path.exists(tf_file)


def test_process_teams_addition(mocker):
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.teams_to_add = [
        {"team_name": "team1", "privacy": "closed",
            "description": "New team", "members": []}
    ]
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_team.assert_called_once_with(
        resource_changes.teams_to_add[0])


def test_process_teams_update(mocker):
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = [
        {"team_name": "team1", "privacy": "closed",
            "description": "Updated team", "members": []}
    ]
    resource_changes.teams_to_delete = []
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_team.assert_called_once_with(
        resource_changes.teams_to_update[0])


def test_process_teams_deletion(mocker):
    output_dir = "terraform"
    os.makedirs(output_dir, exist_ok=True)
    tf_file = os.path.join(output_dir, "team1_team.tf")
    with open(tf_file, "w") as f:
        f.write("dummy")

    resource_changes = MagicMock()
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = [{"team_name": "team1"}]
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=MagicMock())
    process_resources("templates", output_dir, resource_changes)
    assert not os.path.exists(tf_file)


def test_process_memberships_addition(mocker):
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.memberships_to_add = [
        {"username": "user1", "role": "member"}
    ]
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_membership.assert_called_once_with(
        resource_changes.memberships_to_add[0])


def test_process_memberships_update(mocker):
    mock_generator = MagicMock()
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=mock_generator)

    resource_changes = MagicMock()
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = [
        {"username": "user1", "role": "admin"}
    ]
    resource_changes.memberships_to_delete = []
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []

    process_resources("templates", "terraform", resource_changes)
    mock_generator.generate_membership.assert_called_once_with(
        resource_changes.memberships_to_update[0])


def test_process_memberships_deletion(mocker):
    output_dir = "terraform"
    os.makedirs(output_dir, exist_ok=True)
    tf_file = os.path.join(output_dir, "user1_membership.tf")
    with open(tf_file, "w") as f:
        f.write("dummy")

    resource_changes = MagicMock()
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = [{"username": "user1"}]
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []

    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=MagicMock())
    process_resources("templates", output_dir, resource_changes)
    assert not os.path.exists(tf_file)


def test_process_resources_error_handling(mocker):
    # Patch process_repositories で例外を発生させる
    mocker.patch("utils.process_resources.process_repositories",
                 side_effect=Exception("Test error"))
    resource_changes = MagicMock()
    resource_changes.repos_to_add = []
    resource_changes.repos_to_update = []
    resource_changes.repos_to_delete = []
    resource_changes.teams_to_add = []
    resource_changes.teams_to_update = []
    resource_changes.teams_to_delete = []
    resource_changes.memberships_to_add = []
    resource_changes.memberships_to_update = []
    resource_changes.memberships_to_delete = []

    with pytest.raises(Exception) as excinfo:
        process_resources("templates", "terraform", resource_changes)
    assert "Test error" in str(excinfo.value)
