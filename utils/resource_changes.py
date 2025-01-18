class ResourceChanges:
    """
    Represents the changes to be applied to resources (repositories and teams).

    This class encapsulates lists of resources to add, update, or delete, providing
    a structured way to manage changes during Terraform configuration generation.

    Attributes:
        repos_to_add (list[dict]): A list of repositories to add.
        repos_to_update (list[dict]): A list of repositories to update.
        repos_to_delete (list[dict]): A list of repositories to delete.
        teams_to_add (list[dict]): A list of teams to add.
        teams_to_update (list[dict]): A list of teams to update.
        teams_to_delete (list[dict]): A list of teams to delete.

    Example:
        resource_changes = ResourceChanges(
            repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
            repos_to_update=[{"repository_name": "repo2", "visibility": "private"}],
            repos_to_delete=[{"repository_name": "repo3"}],
            teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
            teams_to_update=[{"team_name": "team2", "privacy": "open"}],
            teams_to_delete=[{"team_name": "team3"}]
        )
    """

    def __init__(self, repos_to_add, repos_to_update, repos_to_delete,
                 teams_to_add, teams_to_update, teams_to_delete):
        """
        Initialize the ResourceChanges instance with lists of changes.

        Args:
            repos_to_add (list[dict]): A list of repositories to add, where each dictionary
                contains repository attributes such as `repository_name` and `visibility`.
            repos_to_update (list[dict]): A list of repositories to update, with attributes
                similar to those in `repos_to_add`.
            repos_to_delete (list[dict]): A list of repositories to delete, identified by their `repository_name`.
            teams_to_add (list[dict]): A list of teams to add, where each dictionary contains
                team attributes such as `team_name`, `privacy`, and `members`.
            teams_to_update (list[dict]): A list of teams to update, with attributes
                similar to those in `teams_to_add`.
            teams_to_delete (list[dict]): A list of teams to delete, identified by their `team_name`.

        Example:
            ResourceChanges(
                repos_to_add=[{"repository_name": "repo1", "visibility": "public"}],
                repos_to_update=[],
                repos_to_delete=[{"repository_name": "repo3"}],
                teams_to_add=[{"team_name": "team1", "privacy": "closed"}],
                teams_to_update=[],
                teams_to_delete=[{"team_name": "team2"}]
            )
        """
        self.repos_to_add = repos_to_add
        self.repos_to_update = repos_to_update
        self.repos_to_delete = repos_to_delete
        self.teams_to_add = teams_to_add
        self.teams_to_update = teams_to_update
        self.teams_to_delete = teams_to_delete
