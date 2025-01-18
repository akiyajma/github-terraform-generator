Module generator
================

Sub-modules
-----------
* generator.repository_generator
* generator.team_generator
* generator.terraform_generator

Functions
---------

`generate_repository(repository, template_dir: str, output_dir: str)`
:   Generate a Terraform configuration file for a GitHub repository.
    
    This function takes a repository object or dictionary, validates its attributes, and
    generates a Terraform configuration file using a Jinja2 template. The resulting file
    is saved to the specified output directory.
    
    Args:
        repository (Repository or dict): The repository data, either as a `Repository` object
            or a dictionary with the following keys:
            - `repository_name` (str): The name of the repository.
            - `description` (str, optional): A description of the repository.
            - `visibility` (str): The visibility of the repository (e.g., "public" or "private").
            - `gitignore_template` (str, optional): The Git ignore template to apply.
        template_dir (str): The directory containing the Jinja2 template files.
        output_dir (str): The directory where the generated Terraform file will be saved.
    
    Raises:
        ValueError: If the repository data is invalid.
        TemplateNotFound: If the Jinja2 template file is not found.
        Exception: If an error occurs during template rendering or file writing.
    
    Example:
        >>> repository = {
                "repository_name": "example-repo",
                "description": "An example repository",
                "visibility": "public",
                "gitignore_template": "Python"
            }
        >>> generate_repository(repository, "templates", "output")
    
    Notes:
        - The Jinja2 template file must be named `repository.tf.j2` and located in `template_dir`.
        - The generated file will be saved with the name `<repository_name>_repository.tf` in `output_dir`.

`generate_team(team: models.team.Team, template_dir: str, output_dir: str)`
:   Generate a Terraform configuration file for a GitHub team.
    
    This function takes a `Team` object or a dictionary with team attributes, validates
    the input, and generates a Terraform configuration file by rendering a Jinja2 template.
    The output file is saved in the specified directory.
    
    Args:
        team (Team or dict): A `Team` object or dictionary with the following attributes:
            - `team_name` (str): The name of the team.
            - `description` (str, optional): A description of the team.
            - `privacy` (str): The privacy level of the team (e.g., "closed", "secret").
            - `members` (list[dict], optional): A list of team members, where each member
              is represented as a dictionary with `username` and `role` keys.
        template_dir (str): The directory containing the Jinja2 template files.
        output_dir (str): The directory where the Terraform configuration file will be saved.
    
    Raises:
        ValueError: If the `team` object is invalid or lacks required attributes.
        FileNotFoundError: If the specified template file is not found in `template_dir`.
        Exception: If any error occurs during rendering or file writing.
    
    Example:
        >>> team = Team(
                team_name="dev-team",
                description="Development team",
                privacy="closed",
                members=[{"username": "dev1", "role": "maintainer"}]
            )
        >>> generate_team(team, "templates", "output")
    
    Notes:
        - The Jinja2 template file should be named `team.tf.j2` and located in `template_dir`.
        - The output file will be saved as `<team_name>_team.tf` in the specified `output_dir`.
        - If a dictionary is passed instead of a `Team` object, it will be converted internally.

Classes
-------

`TerraformGenerator(template_dir: str, output_dir: str)`
:   A utility class for generating Terraform configuration files for GitHub repositories and teams.
    
    This class encapsulates the logic for handling repository and team data, validating inputs,
    and generating Terraform configuration files by rendering Jinja2 templates.
    
    Attributes:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.
    
    Example:
        >>> generator = TerraformGenerator(template_dir="templates", output_dir="output")
        >>> generator.generate_repository({"repository_name": "repo1", "visibility": "public"})
        >>> generator.generate_team({"team_name": "team1", "privacy": "closed"})
    
    Initialize the TerraformGenerator.
    
    Args:
        template_dir (str): Path to the directory containing Jinja2 templates.
        output_dir (str): Path to the directory where Terraform files will be generated.
    
    Example:
        >>> generator = TerraformGenerator(template_dir="templates", output_dir="output")

    ### Methods

    `generate_repository(self, repository)`
    :   Generate Terraform configuration files for GitHub repositories.
        
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

    `generate_team(self, team)`
    :   Generate Terraform configuration files for GitHub teams.
        
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