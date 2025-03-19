import os
from unittest.mock import MagicMock, patch

import pytest

from utils.process_resources import (
    process_memberships,
    process_repositories,
    process_resources,
    process_teams,
)

# --- テスト補助用フィクスチャ ---


@pytest.fixture
def dummy_generator():
    """
    TerraformGenerator のダミーインスタンス。各生成メソッドは通常は何もしないが、
    必要に応じて side_effect で例外を発生させることができる。
    """
    gen = MagicMock()
    gen.generate_repository.side_effect = None
    gen.generate_team.side_effect = None
    gen.generate_membership.side_effect = None
    return gen

# --- process_repositories の例外分岐を網羅するテスト ---


def test_process_repositories_add_exception(tmp_path, dummy_generator):
    dummy_generator.generate_repository.side_effect = Exception("Add error")
    repos_to_add = [{
        "repository_name": "repo1",
        "visibility": "public",
        "description": "Test repo",
        "gitignore_template": "Python"
    }]
    with pytest.raises(Exception) as excinfo:
        process_repositories(dummy_generator, str(
            tmp_path), repos_to_add, [], [])
    assert "Error adding repository" in str(excinfo.value)


def test_process_repositories_update_exception(tmp_path, dummy_generator):
    dummy_generator.generate_repository.side_effect = Exception("Update error")
    repos_to_update = [{
        "repository_name": "repo1",
        "visibility": "public",
        "description": "Test repo",
        "gitignore_template": "Python"
    }]
    with pytest.raises(Exception) as excinfo:
        process_repositories(dummy_generator, str(
            tmp_path), [], repos_to_update, [])
    assert "Error updating repository" in str(excinfo.value)


def test_process_repositories_deletion_exception(tmp_path, dummy_generator):
    # ファイル削除時に例外発生させるため、os.remove をパッチする
    repos_to_delete = [{"repository_name": "repo1"}]
    test_file = os.path.join(str(tmp_path), "repo1_repository.tf")
    with open(test_file, "w") as f:
        f.write("dummy")
    with patch("os.remove", side_effect=Exception("Delete error")):
        with pytest.raises(Exception) as excinfo:
            process_repositories(dummy_generator, str(
                tmp_path), [], [], repos_to_delete)
        assert "Error deleting repository" in str(excinfo.value)

# --- process_teams の例外分岐を網羅するテスト ---


def test_process_teams_add_exception(tmp_path, dummy_generator):
    dummy_generator.generate_team.side_effect = Exception("Team add error")
    teams_to_add = [{"team_name": "team1", "privacy": "closed",
                     "description": "Test team", "members": []}]
    with pytest.raises(Exception) as excinfo:
        process_teams(dummy_generator, str(tmp_path), teams_to_add, [], [])
    assert "Error adding team" in str(excinfo.value)


def test_process_teams_update_exception(tmp_path, dummy_generator):
    dummy_generator.generate_team.side_effect = Exception("Team update error")
    teams_to_update = [{"team_name": "team1", "privacy": "closed",
                        "description": "Test team", "members": []}]
    with pytest.raises(Exception) as excinfo:
        process_teams(dummy_generator, str(tmp_path), [], teams_to_update, [])
    assert "Error updating team" in str(excinfo.value)


def test_process_teams_deletion_exception(mocker, tmp_path):
    output_dir = str(tmp_path)
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

    # os.remove をパッチして例外を発生させる
    mocker.patch("os.remove", side_effect=Exception("Team delete error"))

    # process_resources は例外を再送出しないので、ここでは例外は発生しない
    process_resources("templates", output_dir, resource_changes)

    # 削除に失敗したため、ファイルは削除されず存在するはず
    assert os.path.exists(tf_file)

# --- process_memberships の例外分岐を網羅するテスト ---


def test_process_memberships_add_exception(tmp_path, dummy_generator):
    dummy_generator.generate_membership.side_effect = Exception(
        "Membership add error")
    memberships_to_add = [{"username": "user1", "role": "member"}]
    with pytest.raises(Exception) as excinfo:
        process_memberships(dummy_generator, str(
            tmp_path), memberships_to_add, [], [])
    assert "Error adding membership" in str(excinfo.value)


def test_process_memberships_update_exception(tmp_path, dummy_generator):
    dummy_generator.generate_membership.side_effect = Exception(
        "Membership update error")
    memberships_to_update = [{"username": "user1", "role": "member"}]
    with pytest.raises(Exception) as excinfo:
        process_memberships(dummy_generator, str(tmp_path),
                            [], memberships_to_update, [])
    assert "Error updating membership" in str(excinfo.value)


def test_process_memberships_deletion_exception(tmp_path, dummy_generator):
    memberships_to_delete = [{"username": "user1"}]
    test_file = os.path.join(str(tmp_path), "user1_membership.tf")
    with open(test_file, "w") as f:
        f.write("dummy")
    with patch("os.remove", side_effect=Exception("Membership delete error")):
        with pytest.raises(Exception) as excinfo:
            process_memberships(dummy_generator, str(
                tmp_path), [], [], memberships_to_delete)
        assert "Error deleting membership" in str(excinfo.value)

# --- process_resources の正常系および統合テスト ---


def test_process_resources_complete(tmp_path, dummy_generator, mocker):
    # TerraformGenerator のコンストラクタをモックして、dummy_generator を返すようにする
    mocker.patch("utils.process_resources.TerraformGenerator",
                 return_value=dummy_generator)
    resource_changes = mocker.MagicMock()
    resource_changes.repos_to_add = [
        {"repository_name": "repo1", "visibility": "public", "description": "Repo add", "gitignore_template": "Python"}]
    resource_changes.repos_to_update = [
        {"repository_name": "repo1", "visibility": "private", "description": "Repo update", "gitignore_template": "Python"}]
    resource_changes.repos_to_delete = [{"repository_name": "repo1"}]
    resource_changes.teams_to_add = [
        {"team_name": "team1", "privacy": "closed", "description": "Team add", "members": []}]
    resource_changes.teams_to_update = [
        {"team_name": "team1", "privacy": "secret", "description": "Team update", "members": []}]
    resource_changes.teams_to_delete = [{"team_name": "team1"}]
    resource_changes.memberships_to_add = [
        {"username": "user1", "role": "member"}]
    resource_changes.memberships_to_update = [
        {"username": "user1", "role": "admin"}]
    resource_changes.memberships_to_delete = [{"username": "user1"}]

    # 生成済みのファイルを作成して削除分岐を実行
    repo_file = os.path.join(str(tmp_path), "repo1_repository.tf")
    team_file = os.path.join(str(tmp_path), "team1_team.tf")
    membership_file = os.path.join(str(tmp_path), "user1_membership.tf")
    for file_path in [repo_file, team_file, membership_file]:
        with open(file_path, "w") as f:
            f.write("dummy")

    process_resources("templates", str(tmp_path), resource_changes)
    # 削除処理で各ファイルが削除されたことを確認
    assert not os.path.exists(repo_file)
    assert not os.path.exists(team_file)
    assert not os.path.exists(membership_file)
