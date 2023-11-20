from enum import Enum


class AutheneEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class UserRoles(AutheneEnum):
    owner = "Owner"
    member = "Member"
    admin = "Admin"
