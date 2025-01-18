Module main
===========

Functions
---------

`main(output_dir_override=None)`
:   Main function to process and apply changes to the Terraform state.
    
    This function serves as the entry point for managing resources defined in Terraform state.
    It performs the following steps:
    1. Loads the application configuration from `config.yaml`.
    2. Loads the existing Terraform state from the specified file.
    3. Extracts resources (repositories and teams) from the Terraform state.
    4. Compares the extracted resources with the new resources provided via environment variables.
    5. Calculates the differences (additions, updates, deletions) between the existing and new resources.
    6. Applies the changes by generating, updating, or deleting Terraform files.
    
    Args:
        output_dir_override (str, optional): Overrides the output directory specified in the configuration.
            If not provided, the output directory specified in `config.yaml` is used.
    
    Environment Variables:
        REPOSITORIES (str): A JSON-encoded list of repository definitions. Each repository should include:
            - `repository_name` (str): The name of the repository.
            - `description` (str, optional): A description of the repository.
            - `visibility` (str): The visibility of the repository (e.g., "public" or "private").
            - `gitignore_template` (str, optional): The Git ignore template to apply.
        TEAMS (str): A JSON-encoded list of team definitions. Each team should include:
            - `team_name` (str): The name of the team.
            - `description` (str, optional): A description of the team.
            - `privacy` (str): The privacy level of the team (e.g., "closed" or "secret").
            - `members` (list[dict], optional): A list of team members with their roles.
    
    Raises:
        SystemExit: Exits the script with status code 1 if an unhandled error occurs.
    
    Logs:
        - Logs informational messages about the processing steps.
        - Logs errors with details if any step fails.
    
    Example:
        To override the output directory and process changes:
        >>> main(output_dir_override="/custom/output/dir")
    
    Files Used:
        - Configuration: `config/config.yaml`
        - Terraform state: `<output_dir>/terraform.tfstate`
        - Resource changes are saved to `<output_dir>/existing_resources.json`.