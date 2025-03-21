from pydantic import BaseModel, Field


class RepositoryCollaborator(BaseModel):
    """
    Model representing a GitHub repository collaborator.

    This model defines the structure for a GitHub repository collaborator, including
    the repository name, collaborator username, assigned permission level, and whether
    deletion is allowed. It also provides a computed property for generating a unique
    collaborator identifier.

    Attributes:
        repository_name (str): The name of the GitHub repository to which the collaborator is added.
        username (str): The GitHub username of the collaborator.
        permission (str): The permission level assigned to the collaborator.
            Must be one of the following:
            - "pull" (Read access)
            - "push" (Write access)
            - "admin" (Full access)
        allow_delete (bool): A flag indicating whether the collaborator can be removed.
            Defaults to `False`.

    Properties:
        collaborator_id (str): A unique identifier for the collaborator,
            generated by concatenating `repository_name` and `username`
            with an underscore (`_`).

    Example:
        >>> collaborator = RepositoryCollaborator(
        ...     repository_name="example-repo",
        ...     username="dev-user",
        ...     permission="push"
        ... )
        >>> print(collaborator.collaborator_id)
        "example-repo_dev-user"
    """
    repository_name: str
    username: str
    permission: str = Field(..., pattern="^(pull|push|admin)$")
    allow_delete: bool = False

    @property
    def collaborator_id(self) -> str:
        return f"{self.repository_name}_{self.username}"
