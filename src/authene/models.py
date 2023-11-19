from typing import List, Optional

from pydantic import Field

from authene_common.database import Base
from authene_common.models import AutheneBase, Pagination, TimestampMixin


class AutheneUser(Base, TimestampMixin):
    pass


class UserBase(AutheneBase):
    pass


class UserRead(UserBase):
    # id: PrimaryKey
    role: Optional[str] = Field(None)


class UserPagination(Pagination):
    items: List[UserRead]
