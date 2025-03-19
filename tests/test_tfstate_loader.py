import json
import os

import pytest

from utils.tfstate_loader import extract_resources, load_tfstate, save_existing_state


def test_extract_resources_valid():
    """
    正常系: tfstate から repository, team, membership を正しく抽出できることを検証する。
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            "name": "repo1",
                            "description": "Repo description",
                            "visibility": "public",
                            "gitignore_template": "Python"
                        }
                    }
                ]
            },
            {
                "type": "github_team",
                "instances": [
                    {
                        "attributes": {
                            "name": "team1",
                            "description": "Team description",
                            "privacy": "closed"
                        }
                    }
                ]
            },
            {
                "type": "github_membership",
                "instances": [
                    {
                        "attributes": {
                            "username": "user1",
                            "role": "member"
                        }
                    }
                ]
            }
        ]
    }
    result = extract_resources(tfstate)
    assert len(result["repositories"]) == 1
    assert result["repositories"][0]["repository_name"] == "repo1"
    assert len(result["teams"]) == 1
    assert result["teams"][0]["team_name"] == "team1"
    assert len(result["memberships"]) == 1
    assert result["memberships"][0]["username"] == "user1"


def test_extract_resources_keyerror():
    """
    キーが不足している場合に KeyError が発生することを検証する。
    例として、repository の attributes から "name" キーが欠如している場合。
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            # "name" キーがない
                            "description": "No name repo",
                            "visibility": "public",
                            "gitignore_template": "Python"
                        }
                    }
                ]
            }
        ]
    }
    with pytest.raises(KeyError) as excinfo:
        extract_resources(tfstate)
    assert "Missing expected key" in str(excinfo.value)


def test_extract_resources_unexpected_exception():
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                # instances を文字列にして、for ループで AttributeError を発生させる
                "instances": "not a list"
            }
        ]
    }
    with pytest.raises(Exception) as excinfo:
        extract_resources(tfstate)
    assert "Unexpected error extracting resources" in str(excinfo.value)


def test_load_tfstate_file_not_found(tmp_path):
    """
    存在しない tfstate ファイルを指定した場合に FileNotFoundError が発生することを検証する。
    """
    non_existent = tmp_path / "nonexistent.tfstate"
    with pytest.raises(FileNotFoundError):
        load_tfstate(str(non_existent))


def test_load_tfstate_invalid_json(tmp_path):
    """
    無効な JSON の tfstate ファイルを読み込もうとした場合に JSONDecodeError が発生することを検証する。
    """
    file_path = tmp_path / "invalid.tfstate"
    file_path.write_text("not valid json")
    with pytest.raises(json.JSONDecodeError):
        load_tfstate(str(file_path))


def test_load_tfstate_valid(tmp_path):
    """
    正常な tfstate ファイルを読み込み、正しい辞書が返されることを検証する。
    """
    data = {"resources": []}
    file_path = tmp_path / "valid.tfstate"
    file_path.write_text(json.dumps(data))
    result = load_tfstate(str(file_path))
    assert result == data


def test_save_existing_state(tmp_path):
    """
    save_existing_state が正しく JSON ファイルを生成することを検証する。
    """
    state = {
        "repositories": [{"repository_name": "repo1", "visibility": "public", "description": "A repo"}],
        "teams": [{"team_name": "team1", "description": "A team", "privacy": "closed"}]
    }
    file_path = tmp_path / "existing_state.json"
    save_existing_state(state, str(file_path))
    with open(str(file_path), "r") as f:
        loaded = json.load(f)
    assert loaded == state


def test_save_existing_state_oserror(monkeypatch, tmp_path):
    """
    出力ディレクトリ作成時に OSError が発生した場合、適切な例外が発生することを検証する。
    """
    file_path = tmp_path / "existing_state.json"
    # os.makedirs をパッチして OSError を発生させる
    monkeypatch.setattr(os, "makedirs", lambda path, exist_ok=True: (
        _ for _ in ()).throw(OSError("Test OSError")))
    with pytest.raises(OSError) as excinfo:
        save_existing_state({}, str(file_path))
    assert "Failed to save existing state" in str(excinfo.value)
