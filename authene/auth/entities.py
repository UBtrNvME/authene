"""Entities that are part of the authorisation and authentication logic."""
from dataclasses import dataclass


@dataclass
class Credentials:
    """Credentials object that is used for authentication purposes."""

    username: str
    password: str
