import pytest

from generator.membership_generator import generate_membership


class Membership:
    def __init__(self, username):
        self.username = username


@pytest.fixture
def membership():
    return Membership(username="testuser")


def test_generate_membership_create(membership, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir /
     "membership.tf.j2").write_text("{{ membership.username }} {{ action }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_membership(membership, str(template_dir),
                        str(output_dir), action="create")

    output_file = output_dir / "testuser_membership.tf"
    assert output_file.read_text() == "testuser create"


def test_generate_membership_invalid_action(membership, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir /
     "membership.tf.j2").write_text("{{ membership.username }} {{ action }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(ValueError, match="Invalid action. Must be 'create', 'update', or 'delete'."):
        generate_membership(membership, str(template_dir),
                            str(output_dir), action="invalid")


def test_generate_membership_update(membership, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir /
     "membership.tf.j2").write_text("{{ membership.username }} {{ action }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_membership(membership, str(template_dir),
                        str(output_dir), action="update")

    output_file = output_dir / "testuser_membership.tf"
    assert output_file.read_text() == "testuser update"


def test_generate_membership_delete(membership, tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir /
     "membership.tf.j2").write_text("{{ membership.username }} {{ action }}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    generate_membership(membership, str(template_dir),
                        str(output_dir), action="delete")

    output_file = output_dir / "testuser_membership.tf"
    assert output_file.read_text() == "testuser delete"
