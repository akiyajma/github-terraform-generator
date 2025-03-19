class ResourceChanges:
    """
    Represents the planned changes to be applied to resources in Terraform.

    This class provides a structured way to track changes in repositories, teams,
    memberships, and repository collaborators. It contains lists of resources
    categorized into additions, updates, and deletions.

    Attributes:
        repos_to_add (list[dict]): List of repositories to add, each represented as:
            - `repository_name` (str): The name of the repository.
            - `visibility` (str): The repository visibility (e.g., "public", "private").
            - `description` (str, optional): The description of the repository.
            - `gitignore_template` (str, optional): Specifies a `.gitignore` template.
              If set to `"None"`, it is omitted in Terraform configuration.
        repos_to_update (list[dict]): List of repositories to update, following the same structure as `repos_to_add`.
        repos_to_delete (list[dict]): List of repositories to delete, identified by `repository_name`.

        teams_to_add (list[dict]): List of teams to add, each represented as:
            - `team_name` (str): The name of the team.
            - `privacy` (str): The privacy setting (e.g., "closed", "secret").
            - `description` (str, optional): A description of the team.
            - `members` (list[dict], optional): A list of team members, each represented as:
                - `username` (str): The member's username.
                - `role` (str): The member's role in the team (e.g., "maintainer", "member").
        teams_to_update (list[dict]): List of teams to update, following the same structure as `teams_to_add`.
        teams_to_delete (list[dict]): List of teams to delete, identified by `team_name`.

        memberships_to_add (list[dict]): List of user memberships to add, each represented as:
            - `username` (str): The GitHub username.
            - `role` (str): The role of the user in the organization (e.g., "member", "admin").
        memberships_to_update (list[dict]): List of user memberships to update.
        memberships_to_delete (list[dict]): List of user memberships to delete, identified by `username`.

        repo_collaborators_to_add (list[dict]): List of repository collaborators to add, each represented as:
            - `repository_name` (str): The name of the repository.
            - `username` (str): The GitHub username of the collaborator.
            - `permission` (str): The permission level for the collaborator (e.g., "pull", "push", "admin").
        repo_collaborators_to_update (list[dict]): List of repository collaborators to update.
        repo_collaborators_to_delete (list[dict]): List of repository collaborators to delete, identified by `repository_name` and `username`.

    Example:
        resource_changes = ResourceChanges(
            repos_to_add=[
                {"repository_name": "repo1", "visibility": "public", "description": "A new public repository", "gitignore_template": "Python"}
            ],
            repos_to_update=[
                {"repository_name": "repo2", "visibility": "private", "description": "Updated repository", "gitignore_template": "None"}
            ],
            repos_to_delete=[
                {"repository_name": "repo3"}
            ],
            teams_to_add=[
                {"team_name": "team1", "privacy": "closed", "description": "New team", "members": [{"username": "user1", "role": "maintainer"}]}
            ],
            teams_to_update=[
                {"team_name": "team2", "privacy": "secret", "description": "Updated team"}
            ],
            teams_to_delete=[
                {"team_name": "team3"}
            ],
            memberships_to_add=[
                {"username": "user1", "role": "member"}
            ],
            memberships_to_update=[
                {"username": "user2", "role": "admin"}
            ],
            memberships_to_delete=[
                {"username": "user3"}
            ],
            repo_collaborators_to_add=[
                {"repository_name": "repo1", "username": "external_user", "permission": "push"}
            ],
            repo_collaborators_to_update=[
                {"repository_name": "repo1", "username": "external_user", "permission": "admin"}
            ],
            repo_collaborators_to_delete=[
                {"repository_name": "repo2", "username": "old_user"}
            ]
        )
    """

    def __init__(self, repos_to_add, repos_to_update, repos_to_delete,
                 teams_to_add, teams_to_update, teams_to_delete,
                 memberships_to_add, memberships_to_update, memberships_to_delete,
                 repo_collaborators_to_add, repo_collaborators_to_update, repo_collaborators_to_delete):
        """
        Initializes a ResourceChanges instance with categorized resource changes.

        Args:
            repos_to_add (list[dict]): List of repositories to add.
            repos_to_update (list[dict]): List of repositories to update.
            repos_to_delete (list[dict]): List of repositories to delete.
            teams_to_add (list[dict]): List of teams to add.
            teams_to_update (list[dict]): List of teams to update.
            teams_to_delete (list[dict]): List of teams to delete.
            memberships_to_add (list[dict]): List of user memberships to add.
            memberships_to_update (list[dict]): List of user memberships to update.
            memberships_to_delete (list[dict]): List of user memberships to delete.
            repo_collaborators_to_add (list[dict]): List of repository collaborators to add.
            repo_collaborators_to_update (list[dict]): List of repository collaborators to update.
            repo_collaborators_to_delete (list[dict]): List of repository collaborators to delete.

        Example:
            resource_changes = ResourceChanges(
                repos_to_add=[
                    {"repository_name": "repo1", "visibility": "public", "description": "A new public repository", "gitignore_template": "Python"}
                ],
                repos_to_update=[
                    {"repository_name": "repo2", "visibility": "private", "description": "Updated repository", "gitignore_template": "None"}
                ],
                repos_to_delete=[
                    {"repository_name": "repo3"}
                ],
                teams_to_add=[
                    {"team_name": "team1", "privacy": "closed", "description": "New team", "members": [{"username": "user1", "role": "maintainer"}]}
                ],
                teams_to_update=[
                    {"team_name": "team2", "privacy": "secret", "description": "Updated team"}
                ],
                teams_to_delete=[
                    {"team_name": "team3"}
                ],
                memberships_to_add=[
                    {"username": "user1", "role": "member"}
                ],
                memberships_to_update=[
                    {"username": "user2", "role": "admin"}
                ],
                memberships_to_delete=[
                    {"username": "user3"}
                ],
                repo_collaborators_to_add=[
                    {"repository_name": "repo1", "username": "external_user", "permission": "push"}
                ],
                repo_collaborators_to_update=[
                    {"repository_name": "repo1", "username": "external_user", "permission": "admin"}
                ],
                repo_collaborators_to_delete=[
                    {"repository_name": "repo2", "username": "old_user"}
                ]
            )
        """
        self.repos_to_add = repos_to_add
        self.repos_to_update = repos_to_update
        self.repos_to_delete = repos_to_delete
        self.teams_to_add = teams_to_add
        self.teams_to_update = teams_to_update
        self.teams_to_delete = teams_to_delete
        self.memberships_to_add = memberships_to_add
        self.memberships_to_update = memberships_to_update
        self.memberships_to_delete = memberships_to_delete
        self.repo_collaborators_to_add = repo_collaborators_to_add
        self.repo_collaborators_to_update = repo_collaborators_to_update
        self.repo_collaborators_to_delete = repo_collaborators_to_delete
