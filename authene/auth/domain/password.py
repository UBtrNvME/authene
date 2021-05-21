"""Password library for strong hash generation and compare capabilities."""
import secrets
from hashlib import pbkdf2_hmac
from typing import Union

NUMBER_OF_ITERATIONS = 100000
LENGTH_OF_SALT = 128


class __HashPassword:
    """
    Protected class that implements password hashing manipulations.

    Attributes:
          generate_hash
          generate_salt
          compare_password
    """

    @staticmethod
    def generate_hash(password, salt: Union[str, bytes]):
        """Generate cryptographically strong hash out of the password and salt."""
        if isinstance(salt, str):
            salt = salt.encode("utf-8")
        elif not isinstance(salt, bytes):
            raise TypeError("salt should be of type str or bytes")

        a_hash = pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, NUMBER_OF_ITERATIONS
        )
        return salt + a_hash

    @classmethod
    def compare_password(cls, password, candidate):
        """Compare hashed password with candidate password."""
        salt = password[:LENGTH_OF_SALT]
        candidate_pass = cls.generate_hash(candidate, salt)
        return secrets.compare_digest(candidate_pass, password)

    @staticmethod
    def generate_salt():
        """Generate cryptographically random and unique salt for hash password."""
        return secrets.token_hex(LENGTH_OF_SALT)


passwordlib = __HashPassword()
