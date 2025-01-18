Module generator.repository_generator
=====================================

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