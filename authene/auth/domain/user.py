"""Entities that are part of the authorisation and authentication logic."""
from dataclasses import dataclass

from authene.auth.domain.password import passwordlib


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

    def match_password(self, candidate):
        """Match user password with candidate password."""
        return passwordlib.compare_password(self.password, candidate)


@dataclass
class Credentials:
    """Dataclass for Credentials."""

    username: str
    password: str
