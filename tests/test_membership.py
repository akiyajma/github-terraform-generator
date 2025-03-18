import os

import pytest
from pydantic import ValidationError

from generator.membership_generator import generate_membership
from models.membership import Membership


# autouse フィクスチャを使い、各テスト後に生成されたファイルを削除する
@pytest.fixture(autouse=True)
def cleanup_generated_membership_file():
    yield  # テスト実行
    # 出力先ディレクトリ "terraform" 内の user1_membership.tf を削除
    output_path = os.path.join("terraform", "user1_membership.tf")
    if os.path.exists(output_path):
        os.remove(output_path)


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
