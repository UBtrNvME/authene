"""Jwt token manipulation use cases."""
from datetime import datetime, timedelta

import jwt
from usecase import UseCase

JWT_LIFE_SPAN_IN_MINUTES = 60
JWT_ALGORITHM = "HS256"
JWT_SECRET = "secret"


class GenerateToken(UseCase):
    """Generate JWT token."""

    def __init__(self, user_id, **kwargs):
        """Initialise GenerateToken use case."""
        self.user_id = user_id
        self.options = kwargs

    def execute(self):
        """Implement UseCase.execute method."""
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(
            minutes=self.options.get("duration", None) or JWT_LIFE_SPAN_IN_MINUTES
        )

        payload = {
            "uid": self.user_id,
            "iat": issued_at.timestamp(),
            "exp": expires_at.timestamp(),
        }
        return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


class VerifyToken(UseCase):
    """Verify that token was issued by our service."""

    def __init__(self, token):
        """Initialise VerifyToken use case."""
        self.token = token

    def execute(self):
        """Implement UseCase.execute method."""
        try:
            payload = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            print(e)
            return None

        return payload
