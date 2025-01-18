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
:   Generate a Terraform file for a GitHub repository.
    
    Args:
        repository (Repository or dict): The repository object or dictionary containing repository attributes.
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform file will be saved.
    
    Raises:
        ValidationError: If the repository data is invalid.

`generate_team(team: models.team.Team, template_dir: str, output_dir: str)`
:   Generate a Terraform file for a GitHub team.
    
    Args:
        team (Team): The team object containing team attributes.
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform file will be saved.

Classes
-------

`TerraformGenerator(template_dir: str, output_dir: str)`
:   A class to generate Terraform files for GitHub repositories and teams.
    
    Attributes:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.
    
    Initialize the TerraformGenerator with template and output directories.
    
    Args:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.

    ### Methods

    `generate_repository(self, repository)`
    :   Generate a Terraform file for a GitHub repository.
        
        Args:
            repository (Repository or dict): The repository object or dictionary containing repository attributes.

    `generate_team(self, team)`
    :   Generate a Terraform file for a GitHub team.
        
        Args:
            team (Team or dict): The team object or dictionary containing team attributes.