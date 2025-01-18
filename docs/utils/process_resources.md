Module utils.process_resources
==============================

Functions
---------

`process_repositories(generator, output_dir, repos_to_add, repos_to_update, repos_to_delete)`
:   Process the repositories to add, update, and delete.
    
    Args:
        generator (TerraformGenerator): The Terraform generator instance.
        output_dir (str): The directory where the generated Terraform files will be saved.
        repos_to_add (list[Repository]): A list of repositories to add.
        repos_to_update (list[Repository]): A list of repositories to update.
        repos_to_delete (list[Repository]): A list of repositories to delete.

`process_resources(template_dir, output_dir, resource_changes: utils.resource_changes.ResourceChanges)`
:   Process the resources (repositories and teams) to add, update, and delete.
    
    Args:
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform files will be saved.
        resource_changes (ResourceChanges): The changes to be applied to the resources.

`process_teams(generator, output_dir, teams_to_add, teams_to_update, teams_to_delete)`
:   Process the teams to add, update, and delete.
    
    Args:
        generator (TerraformGenerator): The Terraform generator instance.
        output_dir (str): The directory where the generated Terraform files will be saved.
        teams_to_add (list[Team]): A list of teams to add.
        teams_to_update (list[Team]): A list of teams to update.
        teams_to_delete (list[Team]): A list of teams to delete.