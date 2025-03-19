from pydantic import BaseModel, Field


class Repository(BaseModel):
    """
    Model representing a GitHub repository.

    This model defines the structure for a GitHub repository, including its name,
    description, visibility settings, `.gitignore` template, and whether deletion
    is allowed.

    Attributes:
        repository_name (str): The name of the GitHub repository.
        description (str): A brief description of the repository.
        visibility (str): The repository's visibility setting.
            Must be one of the following:
            - "public" (Accessible to everyone)
            - "private" (Restricted access)
            - "internal" (Accessible only within an organization)
        gitignore_template (str): The `.gitignore` template to apply to the repository.
            If set to `"None"`, no `.gitignore` file will be applied.
        allow_delete (bool): A flag indicating whether the repository can be deleted.
            Defaults to `False`.

    Example:
        >>> repo = Repository(
        ...     repository_name="example-repo",
        ...     description="A sample GitHub repository",
        ...     visibility="public",
        ...     gitignore_template="Python"
        ... )
        >>> print(repo.repository_name)
        "example-repo"
    """
    repository_name: str
    description: str
    visibility: str = Field(..., pattern="^(public|private|internal)$")
    gitignore_template: str
    allow_delete: bool = False
