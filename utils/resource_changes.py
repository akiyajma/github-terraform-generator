class ResourceChanges:
    """
    Represents the changes to be applied to resources (repositories and teams).

    This class encapsulates lists of repositories and teams to add, update, or delete,
    providing a structured way to manage changes during Terraform configuration generation.
    It includes attributes like `gitignore_template` and `description` for repositories
    and `description` for teams to ensure detailed resource definitions.

    Attributes:
        repos_to_add (list[dict]): A list of repositories to add, where each dictionary contains:
            - `repository_name` (str): The name of the repository.
            - `visibility` (str): The visibility of the repository (e.g., "public", "private").
            - `description` (str, optional): A description of the repository.
            - `gitignore_template` (str, optional): A template for `.gitignore`. Excluded if set to "None".
        repos_to_update (list[dict]): A list of repositories to update, with similar attributes as `repos_to_add`.
        repos_to_delete (list[dict]): A list of repositories to delete, identified by `repository_name`.
        teams_to_add (list[dict]): A list of teams to add, where each dictionary contains:
            - `team_name` (str): The name of the team.
            - `privacy` (str): The privacy setting of the team (e.g., "closed", "secret").
            - `description` (str, optional): A description of the team.
            - `members` (list[dict], optional): A list of team members, each represented as:
                - `username` (str): The member's username.
                - `role` (str): The member's role in the team (e.g., "maintainer", "member").
        teams_to_update (list[dict]): A list of teams to update, with similar attributes as `teams_to_add`.
        teams_to_delete (list[dict]): A list of teams to delete, identified by `team_name`.

    Example:
        resource_changes = ResourceChanges(
            repos_to_add=[
                {"repository_name": "repo1", "visibility": "public", "description": "A public repo", "gitignore_template": "Python"}
            ],
            repos_to_update=[
                {"repository_name": "repo2", "visibility": "private", "description": "Updated repo", "gitignore_template": "None"}
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
            ]
        )
    """

    def __init__(self, repos_to_add, repos_to_update, repos_to_delete,
                 teams_to_add, teams_to_update, teams_to_delete,
                 memberships_to_add, memberships_to_update, memberships_to_delete,
                 repo_collaborators_to_add, repo_collaborators_to_update, repo_collaborators_to_delete):
        """
        Initialize the ResourceChanges instance with lists of changes.

        Args:
            repos_to_add (list[dict]): A list of repositories to add, where each dictionary
                contains repository attributes such as `repository_name`, `visibility`,
                `description`, and `gitignore_template`. Exclude `gitignore_template` if set to "None".
            repos_to_update (list[dict]): A list of repositories to update, with similar attributes
                as `repos_to_add`.
            repos_to_delete (list[dict]): A list of repositories to delete, identified by `repository_name`.
            teams_to_add (list[dict]): A list of teams to add, where each dictionary contains
                attributes such as `team_name`, `privacy`, `description`, and `members`.
            teams_to_update (list[dict]): A list of teams to update, with similar attributes
                as `teams_to_add`.
            teams_to_delete (list[dict]): A list of teams to delete, identified by `team_name`.

        Example:
            ResourceChanges(
                repos_to_add=[
                    {"repository_name": "repo1", "visibility": "public", "description": "A public repo", "gitignore_template": "Python"}
                ],
                repos_to_update=[
                    {"repository_name": "repo2", "visibility": "private", "description": "Updated repo", "gitignore_template": "None"}
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
