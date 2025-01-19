from pydantic import BaseModel, Field


class Repository(BaseModel):
    """
    A model representing a repository.

    Attributes:
        repository_name (str): The name of the repository.
        description (str): The description of the repository.
        visibility (str): The visibility of the repository (public, private, or internal).
        gitignore_template (str): The gitignore template to use for the repository.
    """
    repository_name: str
    description: str
    visibility: str = Field(..., pattern="^(public|private|internal)$")
    gitignore_template: str
    allow_delete: bool = False
