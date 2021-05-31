"""Password-object that encapsulates password's behavior."""
import hashlib
import secrets
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Password:
    """Password value object."""

    __value: bytes
    __salt: bytes

    @classmethod
    def salt_length(cls):
        return 16

    @property
    def value(self):
        return self.__value

    @property
    def salt(self):
        return self.__salt

    def match_password(self, candidate):
        candidate_hashed = self.generate_hashed_password(candidate, self.__salt)
        return secrets.compare_digest(self.__value, candidate_hashed)

    def change_password(self, new_password):
        return Password.create_from_plain(new_password)

    @classmethod
    def create_from_plain(cls, plain):
        if len(plain) < 8:
            raise ValueError("password length is too short")
        salt = cls._provide_salt()
        hashed = cls.generate_hashed_password(plain, salt=salt)
        return cls(hashed, salt)

    @classmethod
    def generate_hashed_password(cls, password, salt):
        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000, dklen=128
        )
        return hashed

    @classmethod
    def _provide_salt(cls):
        return secrets.token_bytes(cls.salt_length())

    def __repr__(self):
        return f"Password({self.__salt + self.__value})"

    def __str__(self):
        return self.__salt + self.__value

    def __eq__(self, other):
        raise NotImplementedError(
            "Password object's cannot be compared, "
            "use match_password to compare with plain text."
        )
