"""Entities that are part of the authorisation and authentication logic."""
from typing import Optional
from uuid import UUID, uuid4


class Credentials:
    """Credentials object that is used for authentication purposes."""

    def __init__(
        self,
        username: str,
        password: str,
        active: bool = True,
        uuid: Optional[UUID] = None,
    ):
        self.__uuid = uuid or uuid4()
        self.__password = Password(password)
        self.__active = active

        self.username = username


class Password:
    """Password object, that provides all of the methods for easy management."""

    def __init__(self, value):
        self.__value = value

    def __eq__(self, value):
        pass
