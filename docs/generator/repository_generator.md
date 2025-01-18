Module generator.repository_generator
=====================================

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