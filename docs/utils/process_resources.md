Module utils.process_resources
==============================

Functions
---------

`process_repositories(generator, output_dir, repos_to_add, repos_to_update, repos_to_delete)`
:   Handle the lifecycle of repositories: addition, update, and deletion.
    
    This function generates Terraform files for new or updated repositories and removes
    Terraform files for deleted repositories.
    
    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        repos_to_add (list[dict]): A list of repositories to add, represented as dictionaries.
        repos_to_update (list[dict]): A list of repositories to update, represented as dictionaries.
        repos_to_delete (list[dict]): A list of repositories to delete, represented as dictionaries.
    
    Raises:
        Exception: If an error occurs during any repository operation (add, update, delete).
    
    Example:
        process_repositories(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
            repos_to_update=[{"repository_name": "repo2", "visibility": "private"}],
            repos_to_delete=[{"repository_name": "repo3"}]
        )

`process_resources(template_dir, output_dir, resource_changes: utils.resource_changes.ResourceChanges)`
:   Orchestrate the processing of repositories and teams for addition, update, and deletion.
    
    This function delegates repository and team operations to the respective helper functions.
    
    Args:
        template_dir (str): The directory containing Jinja2 templates for Terraform files.
        output_dir (str): The directory where Terraform files will be generated or deleted.
        resource_changes (ResourceChanges): An object containing changes to repositories and teams.
    
    Raises:
        Exception: If an error occurs during repository or team processing.
    
    Example:
        resource_changes = ResourceChanges(
            repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
            repos_to_update=[{"repository_name": "repo2", "visibility": "private"}],
            repos_to_delete=[{"repository_name": "repo3"}],
            teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
            teams_to_update=[],
            teams_to_delete=[{"team_name": "team2"}]
        )
        process_resources(template_dir="templates", output_dir="output", resource_changes=resource_changes)

`process_teams(generator, output_dir, teams_to_add, teams_to_update, teams_to_delete)`
:   Handle the lifecycle of teams: addition, update, and deletion.
    
    This function generates Terraform files for new or updated teams and removes
    Terraform files for deleted teams.
    
    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        teams_to_add (list[dict]): A list of teams to add, represented as dictionaries.
        teams_to_update (list[dict]): A list of teams to update, represented as dictionaries.
        teams_to_delete (list[dict]): A list of teams to delete, represented as dictionaries.
    
    Raises:
        Exception: If an error occurs during any team operation (add, update, delete).
    
    Example:
        process_teams(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
            teams_to_update=[{"team_name": "team2", "privacy": "open"}],
            teams_to_delete=[{"team_name": "team3"}]
        )