from models.repository import Repository
from models.team import Team

from .repository_generator import generate_repository
from .team_generator import generate_team


class TerraformGenerator:
    """
    A class to generate Terraform files for GitHub repositories and teams.

    Attributes:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.
    """

    def __init__(self, template_dir: str, output_dir: str):
        """
        Initialize the TerraformGenerator with template and output directories.

        Args:
            template_dir (str): The directory containing the Jinja2 templates.
            output_dir (str): The directory where the generated Terraform files will be saved.
        """
        self.template_dir = template_dir
        self.output_dir = output_dir

    def generate_repository(self, repository):
        """
        Generate a Terraform file for a GitHub repository.

        Args:
            repository (Repository or dict): The repository object or dictionary containing repository attributes.
        """
        if isinstance(repository, dict):
            repository = Repository(**repository)
        generate_repository(repository, self.template_dir, self.output_dir)

    def generate_team(self, team):
        """
        Generate a Terraform file for a GitHub team.

        Args:
            team (Team or dict): The team object or dictionary containing team attributes.
        """
        if isinstance(team, dict):
            team = Team(**team)
        generate_team(team, self.template_dir, self.output_dir)
