from pydantic import BaseModel, Field


class RepositoryCollaborator(BaseModel):
    repository_name: str
    username: str
    permission: str = Field(..., pattern="^(pull|push|admin)$")
    allow_delete: bool = False

    @property
    def collaborator_id(self) -> str:
        return f"{self.repository_name}_{self.username}"
