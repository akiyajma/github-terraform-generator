class Membership:
    """
    A model representing a GitHub membership.

    Attributes:
        username (str): The GitHub username.
        role (str): The role in the organization (default is "member").
    """

    def __init__(self, username: str, role: str = "member"):
        self.username = username
        self.role = role  # role は渡された値を使い、なければ "member"

    def to_dict(self):
        """
        Convert the Membership object into a dictionary.

        Returns:
            dict: A dictionary representation of the Membership object.
        """
        return {"username": self.username, "role": self.role}
