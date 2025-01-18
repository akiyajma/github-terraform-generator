from typing import List

from pydantic import BaseModel, Field


class TeamMember(BaseModel):
    """
    A model representing a team member.

    Attributes:
        username (str): The username of the team member.
        role (str): The role of the team member (member or maintainer).
    """
    username: str
    role: str = Field(..., pattern="^(member|maintainer)$")


class Team(BaseModel):
    """
    A model representing a team.

    Attributes:
        team_name (str): The name of the team.
        description (str): The description of the team.
        privacy (str): The privacy level of the team (closed, secret, or open).
        members (List[TeamMember]): A list of team members.
    """
    team_name: str
    description: str
    privacy: str = Field(..., pattern="^(closed|secret|open)$")
    members: List[TeamMember]
