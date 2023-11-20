import secrets
import string
from datetime import datetime, timedelta
from typing import List, Optional

import bcrypt
from jose import jwt
from pydantic import EmailStr, validator
from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from authene_common.config import AUTHENE_JWT_ALG, AUTHENE_JWT_EXP, AUTHENE_JWT_SECRET
from authene_common.database import Base
from authene_common.enums import UserRoles
from authene_common.models import AutheneBase, Pagination, PrimaryKey, TimeStampMixin


def generate_password():
    """Generates a reasonable password if none is provided."""
    alphanumeric = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphanumeric) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)  # noqa
            and sum(c.isdigit() for c in password) >= 3  # noqa
        ):
            break
    return password


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class AutheneUser(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    last_mfa_time = Column(DateTime, nullable=True)
    role = Column(String, nullable=True)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=AUTHENE_JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, AUTHENE_JWT_SECRET, algorithm=AUTHENE_JWT_ALG)


class UserBase(AutheneBase):
    email: EmailStr

    @validator("email")
    def email_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string and must be an email")
        return v


class UserLogin(UserBase):
    password: str

    @validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserRegister(UserLogin):
    password: Optional[str] = None

    @validator("password", pre=True, always=True)
    def password_required(cls, v):
        password = v or generate_password()
        return hash_password(password)


class UserLoginResponse(AutheneBase):
    token: Optional[str] = None


class UserRead(UserBase):
    id: PrimaryKey
    role: Optional[str] = UserRoles.admin


class UserUpdate(AutheneBase):
    id: PrimaryKey
    password: Optional[str] = None
    role: Optional[str] = UserRoles.admin

    @validator("password", pre=True)
    def hash(cls, v):
        return hash_password(str(v))


class UserCreate(AutheneBase):
    email: EmailStr
    password: Optional[str] = None
    role: Optional[str] = UserRoles.admin

    @validator("password", pre=True)
    def hash(cls, v):
        return hash_password(str(v))


class UserRegisterResponse(AutheneBase):
    token: Optional[str] = None


class UserPagination(Pagination):
    items: List[UserRead]
