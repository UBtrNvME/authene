"""Entities that are part of the authorisation and authentication logic."""
from dataclasses import dataclass


class User:
    """Credentials object that is used for authentication purposes."""

    def __init__(
        self, email, password, first_name, last_name, username
    ):  # pylint: disable=too-many-arguments
        """Initialise User instance."""
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password


@dataclass
class Credentials:
    """Dataclass for Credentials."""

    username: str
    password: str
