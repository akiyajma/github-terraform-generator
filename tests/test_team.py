import pytest
from pydantic import ValidationError

from models.team import Team


def test_team_model_valid():
    """
    有効な Team モデルが正しく生成されることを検証します。
    """
    data = {
        "team_name": "team1",
        "description": "Team1 description",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "maintainer"}]
    }
    team = Team(**data)
    assert team.team_name == "team1"
    assert team.privacy == "closed"
    # メンバーは Pydantic モデルに変換されている場合
    # もし単なる辞書のままであれば、下記のようにアクセスしてください：
    # assert team.members[0]["username"] == "user1"
    # ここではテスト用に属性アクセスを試みます
    assert hasattr(team.members[0], "username")
    assert team.members[0].username == "user1"


def test_team_model_invalid_member_role():
    """
    無効なメンバーの role を指定した場合に ValidationError が発生することを検証します。
    """
    data = {
        "team_name": "team1",
        "description": "Team1 description",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "invalid"}]
    }
    with pytest.raises(ValidationError):
        Team(**data)
