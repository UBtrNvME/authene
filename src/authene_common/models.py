from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr, conint, constr
from sqlalchemy import Boolean, Column, DateTime, String, event

PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow())
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow())
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


class ContactMixin(TimeStampMixin):
    """Contact mixin"""

    is_active = Column(Boolean, default=True)
    is_external = Column(Boolean, default=False)
    contact_type = Column(String)
    email = Column(String)
    company = Column(String)
    notes = Column(String)
    owner = Column(String)


class AutheneBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Pagination(AutheneBase):
    itemsPerPage: int
    page: int
    total: int


class PrimaryKeyModel(AutheneBase):
    id: PrimaryKey


class ResourceBase(AutheneBase):
    resource_type: Optional[str] = Field(None)
    resource_id: Optional[str] = Field(None)
    weblink: Optional[str] = Field(None)


class ContactBase(DispatchBase):
    email: EmailStr
    name: Optional[str] = Field(None)
    is_active: Optional[bool] = True
    is_external: Optional[bool] = False
    company: Optional[str] = Field(None)
    contact_type: Optional[str] = Field(None)
    notes: Optional[str] = Field(None)
    owner: Optional[str] = Field(None)
