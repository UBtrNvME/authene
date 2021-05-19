"""Use cases related to User entity.

All operations with user should be handled in here.
"""
from token_usecase import GenerateToken

from authene.auth.usecases.usecase import UseCase


class RegisterUser(UseCase):
    """Use cases that handles user registration."""

    def __init__(self, repo, user):
        """Initialise RegisterUser use case."""
        self.repo = repo
        self.user = user

    def execute(self):
        """Implement UseCase.execute method."""
        self.repo.create(self.user)


class AuthenticateUser(UseCase):
    """Use case that handles user authentification."""

    def __init__(self, repo, credentials):
        """Initialise AuthenticateUser use case."""
        self.repo = repo
        self.credentials = credentials

    def execute(self):
        """Implement UseCase.execute method."""
        try:
            user = self.repo.get(username=self.credentials.username)
        # TODO: make this specific! (ubtrnvme, tomorrow)
        except Exception:  # pylint: disable=broad-except

            return None

        return GenerateToken(user.id).execute()
