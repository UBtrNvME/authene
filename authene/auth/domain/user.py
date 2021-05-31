import uuid
from abc import ABCMeta, abstractmethod

from authene.auth.domain.password import Password
from authene.auth.domain.username import Username
from authene.base.entity import Entity


class User(Entity):
    def __init__(self, entity_id, entity_version, username, password):
        super().__init__(entity_id, entity_version)
        self.username = username
        self.password = password

    @classmethod
    def register_user(cls, username, password):
        username = Username(username)
        password = Password.create_from_plain(password)
        return cls(
            entity_version=0,
            entity_id=cls.generate_uuid(),
            username=username,
            password=password,
        )

    @classmethod
    def generate_uuid(cls):
        return "user-{}".format(uuid.uuid4())


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_username(self, username):
        """Find user by his/her username."""
