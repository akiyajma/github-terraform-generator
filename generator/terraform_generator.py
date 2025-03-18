from models.membership import Membership
from models.repository import Repository
from models.team import Team

from .membership_generator import generate_membership
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
        >>> generator.generate_repository({"repository_name": "repo1", "visibility": "public", "gitignore_template": "Python"})
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

        This method generates Terraform configuration files for one or multiple GitHub repositories.
        Each repository's configuration is rendered using a Jinja2 template and saved to the specified
        output directory. If `gitignore_template` is explicitly set to `"None"`, it will be excluded
        from the rendered Terraform configuration.

        Args:
            repository (Repository or dict or list[dict]): Repository data provided as:
                - A single `Repository` object.
                - A dictionary with the following attributes:
                    - `repository_name` (str): The name of the repository (required).
                    - `visibility` (str): The repository's visibility (e.g., "public", "private", "internal") (required).
                    - `description` (str, optional): A brief description of the repository. Defaults to `None` if not specified.
                    - `gitignore_template` (str, optional): Specifies a `.gitignore` template to apply. If `"None"`, this attribute is excluded.
                - A list of dictionaries or `Repository` objects.

        Raises:
            ValueError: If the repository data is missing required attributes or contains invalid values.
            Exception: If any error occurs during template rendering or file generation.

        Example:
            Generate a single repository configuration:
            >>> generator = TerraformGenerator("templates", "output")
            >>> generator.generate_repository({
                "repository_name": "repo1",
                "visibility": "public",
                "description": "A public repository",
                "gitignore_template": "Python"
            })

            Generate multiple repository configurations:
            >>> generator.generate_repository([
                {
                    "repository_name": "repo2",
                    "visibility": "private",
                    "description": "A private repository",
                    "gitignore_template": "Go"
                },
                {
                    "repository_name": "repo3",
                    "visibility": "public",
                    "description": "Another public repository",
                    "gitignore_template": "None"
                }
            ])

        Notes:
            - If `description` is not provided, a default value (e.g., from `config.yaml`) will be applied.
            - If `gitignore_template` is `"None"`, the key is omitted in the generated Terraform file.
            - The output file for each repository is named `<repository_name>_repository.tf` and saved in the `output_dir`.
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

    def generate_membership(self, membership):
        """
        GitHub Membership の Terraform ファイルを生成する

        Args:
            membership (Membership or dict or list[dict]): Membership データ
        """
        try:
            if isinstance(membership, list):
                for m in membership:
                    self.generate_membership(m)
                return

            if isinstance(membership, dict):
                membership = Membership(**membership)

            generate_membership(membership, self.template_dir, self.output_dir)
        except Exception as e:
            username = getattr(membership, "username", "unknown")
            raise Exception(
                f"Error generating Terraform file for membership '{username}': {e}") from e
