from typing import List

from pydantic import BaseModel, Field


class TeamMember(BaseModel):
    """
    Model representing a GitHub team member.

    This model defines the structure for a GitHub team member, including their username
    and role within the team.

    Attributes:
        username (str): The username of the GitHub team member.
        role (str): The role of the team member within the team.
            Must be one of the following:
            - "member" (Standard team member)
            - "maintainer" (Has administrative privileges over the team)

    Example:
        >>> member = TeamMember(username="user1", role="maintainer")
        >>> print(member.username)
        "user1"
    """
    username: str
    role: str = Field(..., pattern="^(member|maintainer)$")


class Team(BaseModel):
    """
    Model representing a GitHub team.

    This model defines the structure for a GitHub team, including its name, description,
    privacy settings, list of members, and whether deletion is allowed.

    Attributes:
        team_name (str): The name of the GitHub team.
        description (str): A brief description of the team.
        privacy (str): The privacy level of the team.
            Must be one of the following:
            - "closed" (Visible within the organization, but only invited members can join)
            - "secret" (Hidden team, only visible to its members)
            - "open" (Anyone in the organization can join)
        members (List[TeamMember]): A list of team members, each defined by the `TeamMember` model.
        allow_delete (bool): A flag indicating whether the team can be deleted.
            Defaults to `False`.

    Example:
        >>> team = Team(
        ...     team_name="dev-team",
        ...     description="Development team responsible for backend services",
        ...     privacy="closed",
        ...     members=[
        ...         TeamMember(username="user1", role="maintainer"),
        ...         TeamMember(username="user2", role="member")
        ...     ]
        ... )
        >>> print(team.team_name)
        "dev-team"
    """
    team_name: str
    description: str
    privacy: str = Field(..., pattern="^(closed|secret|open)$")
    members: List[TeamMember]
    allow_delete: bool = False
