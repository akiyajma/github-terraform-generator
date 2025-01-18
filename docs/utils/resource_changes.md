Module utils.resource_changes
=============================

Classes
-------

`ResourceChanges(repos_to_add, repos_to_update, repos_to_delete, teams_to_add, teams_to_update, teams_to_delete)`
:   A class to represent the changes to be applied to resources (repositories and teams).
    
    Attributes:
        repos_to_add (list): A list of repositories to add.
        repos_to_update (list): A list of repositories to update.
        repos_to_delete (list): A list of repositories to delete.
        teams_to_add (list): A list of teams to add.
        teams_to_update (list): A list of teams to update.
        teams_to_delete (list): A list of teams to delete.
    
    Initialize the ResourceChanges with the lists of changes.
    
    Args:
        repos_to_add (list): A list of repositories to add.
        repos_to_update (list): A list of repositories to update.
        repos_to_delete (list): A list of repositories to delete.
        teams_to_add (list): A list of teams to add.
        teams_to_update (list): A list of teams to update.
        teams_to_delete (list): A list of teams to delete.