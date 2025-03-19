import os

import pytest
from pydantic import ValidationError

from generator.membership_generator import generate_membership
from models.membership import Membership


# 一時的なテンプレートディレクトリを作成し、membership.tf.j2 テンプレートを用意するフィクスチャ
@pytest.fixture
def temp_template_dir(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template_file = templates_dir / "membership.tf.j2"
    # 簡単なテンプレート。membership の username, role, action をレンダリングする
    template_file.write_text(
        'resource "github_membership" "{{ membership.username }}" {\n'
        '  role = "{{ membership.role }}"\n'
        '  action = "{{ action }}"\n'
        '}\n'
    )
    return str(templates_dir)

# 一時的な出力ディレクトリを作成するフィクスチャ


@pytest.fixture
def temp_output_dir(tmp_path):
    output_dir = tmp_path / "terraform"
    output_dir.mkdir()
    return str(output_dir)

# autouse フィクスチャ: テスト終了後に生成された membership ファイルを削除


@pytest.fixture(autouse=True)
def cleanup_generated_file(temp_output_dir):
    yield
    membership_file = os.path.join(temp_output_dir, "user1_membership.tf")
    if os.path.exists(membership_file):
        os.remove(membership_file)


def test_membership_model_valid():
    """
    有効な Membership モデルが正しく生成されることを検証します。
    """
    membership = Membership(username="user1", role="member")
    assert membership.username == "user1"
    assert membership.role == "member"
    assert membership.allow_delete is False


def test_membership_model_invalid_role():
    """
    無効な role を指定した場合に ValidationError が発生することを検証します。
    """
    with pytest.raises(ValidationError):
        Membership(username="user1", role="invalid")


def test_generate_membership_valid(temp_template_dir, temp_output_dir):
    """
    有効な Membership で Terraform ファイルが正しく生成されることを検証します。
    """
    membership = Membership(username="user1", role="member")
    generate_membership(membership, temp_template_dir,
                        temp_output_dir, action="create")
    output_file = os.path.join(temp_output_dir, "user1_membership.tf")
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
    # テンプレートにより、membership の情報および action がレンダリングされているか確認
    assert 'resource "github_membership" "user1"' in content
    assert 'role = "member"' in content
    assert 'action = "create"' in content


def test_generate_membership_invalid_action(temp_template_dir, temp_output_dir):
    """
    無効な action を指定した場合に ValueError が発生することを検証します。
    """
    membership = Membership(username="user1", role="member")
    with pytest.raises(ValueError):
        generate_membership(membership, temp_template_dir,
                            temp_output_dir, action="invalid")
