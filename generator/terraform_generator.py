from models.membership import Membership
from models.repository import Repository
from models.repository_collaborator import RepositoryCollaborator
from models.team import Team

from .membership_generator import generate_membership
from .repository_collaborator_generator import generate_repository_collaborator
from .repository_generator import generate_repository
from .team_generator import generate_team


class TerraformGenerator:
    """
    A utility class for generating Terraform configuration files for GitHub resources.

    This class provides methods to generate Terraform configuration files for GitHub repositories,
    teams, memberships, and repository collaborators. It processes the provided data and
    renders Jinja2 templates to generate the necessary Terraform files.

    Attributes:
        template_dir (str): The directory containing Jinja2 template files.
        output_dir (str): The directory where the generated Terraform configuration files will be stored.

    Example:
        >>> generator = TerraformGenerator(template_dir="templates", output_dir="output")
        >>> generator.generate_repository({"repository_name": "repo1", "visibility": "public", "gitignore_template": "Python"})
        >>> generator.generate_team({"team_name": "team1", "privacy": "closed"})
    """

    def __init__(self, template_dir: str, output_dir: str):
        """
        Initializes the TerraformGenerator instance.

        Args:
            template_dir (str): Path to the directory containing Jinja2 templates.
            output_dir (str): Path to the directory where Terraform configuration files will be generated.

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
        Generates a Terraform configuration file for GitHub memberships.

        This method creates Terraform configuration files for GitHub memberships, linking users to organizations or teams.

        Args:
            membership (Membership or dict or list[dict]): Membership data as:
                - A single `Membership` object.
                - A dictionary containing:
                    - `username` (str): GitHub username.
                    - `role` (str): User role (e.g., "member", "admin").
                - A list of membership dictionaries or `Membership` objects.

        Raises:
            Exception: If an error occurs during template rendering or file creation.

        Example:
            >>> generator = TerraformGenerator("templates", "output")
            >>> generator.generate_membership({
                "username": "user1",
                "role": "member"
            })
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

    def generate_repository_collaborator(self, repository_collaborator):
        """
        Generates a Terraform configuration file for GitHub repository collaborators.

        This method creates Terraform configuration files for one or multiple repository collaborators,
        defining their access permissions.

        Args:
            repository_collaborator (RepositoryCollaborator or dict or list[dict]): Collaborator data as:
                - A single `RepositoryCollaborator` object.
                - A dictionary containing:
                    - `repository_name` (str): Repository name.
                    - `username` (str): Collaborator's GitHub username.
                    - `permission` (str): Permission level (e.g., "pull", "push", "admin").
                - A list of repository collaborator dictionaries or `RepositoryCollaborator` objects.

        Raises:
            Exception: If an error occurs during template rendering or file creation.

        Example:
            >>> generator = TerraformGenerator("templates", "output")
            >>> generator.generate_repository_collaborator({
                "repository_name": "example-repo",
                "username": "collab-user",
                "permission": "push"
            })
        """
        try:
            if isinstance(repository_collaborator, list):
                for rc in repository_collaborator:
                    self.generate_repository_collaborator(rc)
                return

            if isinstance(repository_collaborator, dict):
                repository_collaborator = RepositoryCollaborator(
                    **repository_collaborator)

            generate_repository_collaborator(
                repository_collaborator, self.template_dir, self.output_dir)
        except Exception as e:
            username = getattr(repository_collaborator, "username", "unknown")
            repo = getattr(repository_collaborator,
                           "repository_name", "unknown")
            raise Exception(
                f"Error generating Terraform file for repository collaborator '{username}' on repository '{repo}': {e}") from e
