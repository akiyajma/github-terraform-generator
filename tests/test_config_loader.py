import pytest

from config.config_loader import load_config


@pytest.fixture
def mock_config_file(tmpdir):
    """Create a mock configuration file for testing"""
    config_content = """
    template_dir: "templates"
    output_dir: "terraform"
    default_repository:
      visibility: "public"
    default_team:
      privacy: "closed"
      role: "member"
    """
    config_path = tmpdir.join("config.yaml")
    config_path.write(config_content)
    return str(config_path)


def test_load_config(mock_config_file):
    """
    Test the load_config function.

    Test Cases:
    1. Verify that the 'template_dir' is correctly loaded from the config file.
    2. Verify that the 'output_dir' is correctly loaded from the config file.
    3. Verify that 'default_repository' is present in the loaded config.
    4. Verify that 'default_team' is present in the loaded config.
    """
    config = load_config(mock_config_file)
    assert config["template_dir"] == "templates"
    assert config["output_dir"] == "terraform"
    assert "default_repository" in config
    assert "default_team" in config
