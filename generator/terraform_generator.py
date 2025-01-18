from models.repository import Repository
from models.team import Team

from .repository_generator import generate_repository
from .team_generator import generate_team


class TerraformGenerator:
    """
    A utility class for generating Terraform configuration files for GitHub repositories and teams.

    This class encapsulates the logic for handling repository and team data, validating inputs,
    and generating Terraform configuration files by rendering Jinja2 templates.

    Attributes:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.

    Example:
        >>> generator = TerraformGenerator(template_dir="templates", output_dir="output")
        >>> generator.generate_repository({"repository_name": "repo1", "visibility": "public"})
        >>> generator.generate_team({"team_name": "team1", "privacy": "closed"})
    """

    def __init__(self, template_dir: str, output_dir: str):
        """
        Initialize the TerraformGenerator.

        Args:
            template_dir (str): Path to the directory containing Jinja2 templates.
            output_dir (str): Path to the directory where Terraform files will be generated.

        Example:
            >>> generator = TerraformGenerator(template_dir="templates", output_dir="output")
        """
        self.template_dir = template_dir
        self.output_dir = output_dir

    def generate_repository(self, repository):
        """
        Generate Terraform configuration files for GitHub repositories.

        If a single repository object is provided, it generates one configuration file.
        If a list of repositories is provided, it generates files for all repositories in the list.

        Args:
            repository (Repository or dict or list[dict]): A single repository object,
                dictionary, or a list of dictionaries containing attributes:
                - `repository_name` (str): The name of the repository.
                - `visibility` (str): The visibility of the repository (e.g., "public", "private").
                - `description` (str, optional): A description of the repository.
                - `gitignore_template` (str, optional): A template for `.gitignore`.

        Raises:
            ValueError: If the repository data is invalid.
            Exception: If there is an error during file generation.

        Example:
            >>> generator = TerraformGenerator("templates", "output")
            >>> generator.generate_repository({"repository_name": "repo1", "visibility": "public"})
            >>> generator.generate_repository([
                {"repository_name": "repo2", "visibility": "private"},
                {"repository_name": "repo3", "visibility": "public"}
            ])
        """
        try:
            if isinstance(repository, list):
                for repo in repository:
                    self.generate_repository(repo)
                return

            # Validate and convert repository data
            if isinstance(repository, dict):
                repository = Repository(**repository)

            # Generate the Terraform file
            generate_repository(repository, self.template_dir, self.output_dir)
        except Exception as e:
            repo_name = getattr(repository, "repository_name", "unknown") if not isinstance(
                repository, list) else "list"
            raise Exception(f"Error generating Terraform file for repository '{
                            repo_name}'. {e}") from e

    def generate_team(self, team):
        """
        Generate Terraform configuration files for GitHub teams.

        Args:
            team (Team or dict): A single team object or dictionary containing attributes:
                - `team_name` (str): The name of the team.
                - `description` (str, optional): A description of the team.
                - `privacy` (str): The privacy setting of the team (e.g., "closed", "secret").
                - `members` (list[dict], optional): A list of members where each member
                  is represented as a dictionary with `username` and `role` keys.

        Raises:
            ValueError: If the team data is invalid or missing required attributes.
            RuntimeError: If an error occurs during file generation.

        Example:
            >>> generator = TerraformGenerator("templates", "output")
            >>> generator.generate_team({
                "team_name": "dev-team",
                "privacy": "closed",
                "description": "Development team",
                "members": [{"username": "user1", "role": "maintainer"}]
            })
        """
        try:
            # Validate and convert team data
            if isinstance(team, dict):
                team = Team(**team)
        except Exception as e:
            raise ValueError(f"Invalid team data: {team}. {e}")

        try:
            # Generate the Terraform file
            generate_team(team, self.template_dir, self.output_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to generate team Terraform file: {
                               team.team_name}. {e}")
