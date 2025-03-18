import os

import pytest
from pydantic import ValidationError

from generator.membership_generator import generate_membership
from generator.repository_generator import generate_repository
from models.membership import Membership
from models.repository import Repository


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

# Membership モデルのテスト


def test_membership_model_valid():
    """
    有効な Membership モデルが正しく生成されることを検証します。
    """
    membership = Membership(username="user1", role="member")
    assert membership.username == "user1"
    assert membership.role == "member"
    # allow_delete はデフォルトで False
    assert membership.allow_delete is False


def test_membership_model_valid_admin():
    """
    role に "admin" を指定した場合の検証。
    """
    membership = Membership(username="admin_user",
                            role="admin", allow_delete=True)
    assert membership.username == "admin_user"
    assert membership.role == "admin"
    assert membership.allow_delete is True


def test_membership_model_invalid_role():
    """
    無効な role を指定した場合に ValidationError が発生することを検証します。
    """
    with pytest.raises(ValidationError):
        Membership(username="user_invalid", role="invalid")

# generate_membership() のテスト


def test_generate_membership_valid():
    """
    有効な Membership で Terraform ファイルが正しく生成されることを検証します。
    """
    membership = Membership(username="user1", role="member")
    template_dir = "templates"
    output_dir = "terraform"
    # action 引数が "create" の場合にファイル生成を実行
    generate_membership(membership, template_dir, output_dir, action="create")
    output_path = os.path.join(
        output_dir, f"{membership.username}_membership.tf")
    assert os.path.exists(output_path)
    with open(output_path, "r") as file:
        content = file.read()
        # 生成されたファイルに "resource" という文字列が含まれているか確認
        assert "resource" in content


def test_generate_membership_invalid_action():
    """
    無効なアクションを指定した場合に ValueError が発生することを検証します。
    """
    membership = Membership(username="user1", role="member")
    with pytest.raises(ValueError):
        generate_membership(membership, "templates",
                            "terraform", action="invalid")

# Repository モデル・生成処理のテスト


def test_generate_repository_valid():
    """
    有効な Repository で Terraform ファイルが正しく生成されることを検証します。
    """
    repository = Repository(
        repository_name="example-repo",
        description="An example repository",
        visibility="public",
        gitignore_template="Python"
    )
    template_dir = "templates"
    output_dir = "terraform"
    generate_repository(repository, template_dir, output_dir)
    output_path = os.path.join(
        output_dir, f"{repository.repository_name}_repository.tf")
    assert os.path.exists(output_path)
    with open(output_path, "r") as file:
        content = file.read()
        assert "resource" in content


def test_generate_repository_invalid():
    """
    無効な Repository データ（空の dict）を指定した場合に例外が発生することを検証します。
    """
    with pytest.raises(Exception):
        generate_repository({}, "templates", "terraform")


def test_generate_repository_template_not_found():
    """
    テンプレートが見つからない場合に例外が発生することを検証します。
    """
    repository = Repository(
        repository_name="example-repo",
        description="An example repository",
        visibility="public",
        gitignore_template="Python"
    )
    with pytest.raises(Exception):
        generate_repository(repository, "invalid_templates", "terraform")


def test_generate_repository_file_write_error(mocker):
    """
    ファイル書き込みエラーが発生した場合に例外が発生することを検証します。
    """
    repository = Repository(
        repository_name="example-repo",
        description="An example repository",
        visibility="public",
        gitignore_template="Python"
    )
    mocker.patch("builtins.open", side_effect=PermissionError)
    with pytest.raises(Exception):
        generate_repository(repository, "templates", "terraform")
