import logging

from starlette.config import Config

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)

AUTHENE_JWT_SECRET = config("AUTHENE_JWT_SECRET", default=None)
AUTHENE_JWT_ALG = config("AUTHENE_JWT_ALG", default="HS256")
AUTHENE_JWT_EXP = config("AUTHENE_JWT_EXP", cast=int, default=86400)  # Seconds

STATIC_DIR = config("STATIC_DIR", default=None)

AUTHENE_AUTH_REGISTRATION_ENABLED = config(
    "AUTHENE_AUTH_REGISTRATION_ENABLED", default=False
)

SQLALCHEMY_DATABASE_URI = f"sqlite:///foo.db"
