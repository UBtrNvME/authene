from unittest import TestCase
from authene.auth.domain.user import User
from authene.infrastructure.repositories.user_repo import InMemoryRepository


class TestUser(TestCase):
    def test_register_user(self):
        user = User.register_user("mooniron", "03101998Aiaienvyme")
        self.assertEqual(
            user.version, 0, "User created using factory should have version zero"
        )
        self.assertEqual(
            user.discarded, False, "Just created user should not be discarded"
        )
        self.assertEqual(
            user.instance_id, 0, "Just created user should have instance id of 0"
        )

    def test_generate_uuid(self):
        uuid1 = User.generate_uuid()
        self.assertTrue(uuid1.startswith("user-"), "UUID should start with `user-`")
