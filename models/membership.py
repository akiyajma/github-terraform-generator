from pydantic import BaseModel, Field


class Membership(BaseModel):
    """
    Model representing a GitHub membership.

    This model defines the structure for a GitHub membership, including the username,
    membership role, and whether deletion is allowed. It ensures that the role is
    either "member" or "admin" using validation constraints.

    Attributes:
        username (str): The GitHub username of the member.
        role (str): The membership role, which must be either "member" or "admin".
        allow_delete (bool): A flag indicating whether the membership can be deleted.
            Defaults to `False`.

    Example:
        >>> membership = Membership(username="user1", role="admin", allow_delete=True)
        >>> print(membership)
        Membership(username='user1', role='admin', allow_delete=True)
    """
    username: str
    role: str = Field(..., pattern="^(member|admin)$")
    allow_delete: bool = False
