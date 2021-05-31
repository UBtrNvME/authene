from unittest import TestCase
from authene.infrastructure.repositories.user_repo import InMemoryRepository
from authene.auth.domain.user import User


class TestInMemoryRepository(TestCase):
    def test_find_by_username(self):
        pass

    def test_add(self):
        user = User.register_user("mooniron", "03101998Aiaienvyme")
        repo = InMemoryRepository()
        repo.add(user)
        self.assertTrue(
            repo.find_by_username("mooniron") == user,
            "In memory repo should have a reference.",
        )

