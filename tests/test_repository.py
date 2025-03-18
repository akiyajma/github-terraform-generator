import pytest
from pydantic import ValidationError

from models.repository import Repository


def test_repository_model_valid():
    """
    有効な Repository モデルが正しく生成されることを検証します。
    """
    data = {
        "repository_name": "repo1",
        "description": "Repo1 description",
        "visibility": "public",
        "gitignore_template": "Python"
    }
    repo = Repository(**data)
    assert repo.repository_name == "repo1"
    assert repo.visibility == "public"
    assert repo.gitignore_template == "Python"


def test_repository_model_invalid_visibility():
    """
    無効な visibility を指定した場合に ValidationError が発生することを検証します。
    """
    data = {
        "repository_name": "repo1",
        "description": "Repo1 description",
        "visibility": "invalid",
        "gitignore_template": "Python"
    }
    with pytest.raises(ValidationError):
        Repository(**data)
