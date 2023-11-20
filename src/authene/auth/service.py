import logging
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from authene.models import AutheneUser, UserCreate, UserRegister, UserUpdate
from authene_common.config import AUTHENE_AUTH_REGISTRATION_ENABLED, AUTHENE_JWT_SECRET
from authene_common.enums import UserRoles

logger = logging.getLogger(__name__)


InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


class BasicAuthProviderPlugin(object):
    def get_current_user(self, request: Request, **kwargs):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            logger.exception(
                f"Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}"
            )
            return

        token = authorization.split()[1]

        try:
            data = jwt.decode(token, AUTHENE_JWT_SECRET)
        except (JWKError, JWTError):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=[{"msg": "Could not validate credentials"}],
            ) from None
        return data["email"]


auth_provider = BasicAuthProviderPlugin()


def get_all(*, db_session: Session, filter=None):
    query = db_session.query(AutheneUser)
    if filter:
        query.filter(filter)

    return query.all()


def get(*, db_session: Session, user_id: int) -> Optional[AutheneUser]:
    return db_session.query(AutheneUser).filter(AutheneUser.id == user_id).one_or_none()


def get_by_email(*, db_session: Session, email: str) -> Optional[AutheneUser]:
    return (
        db_session.query(AutheneUser).filter(AutheneUser.email == email).one_or_none()
    )


def create(*, db_session: Session, user_in: (UserRegister | UserCreate)) -> AutheneUser:
    password = bytes(user_in.password, "utf-8")
    user = AutheneUser(
        **user_in.model_dump(exclude={"password", "role"}), password=password
    )

    role = UserRoles.member
    if hasattr(user_in, "role"):
        role = user_in.role
    user.role = role

    db_session.add(user)
    db_session.commit()
    return user


def get_or_create(*, db_session: Session, user_in: UserRegister) -> AutheneUser:
    user = get_by_email(db_session=db_session, email=user_in.email)
    if not user:
        try:
            user = create(db_session=db_session, user_in=user_in)
        except IntegrityError:
            db_session.rollback()
            logger.exception(
                "Unable to create user with email address %s", user_in.email
            )
    return user


def update(
    *, db_session: Session, user: AutheneUser, user_in: UserUpdate
) -> AutheneUser:
    user_data = user.dict()

    update_data = user_in.model_dump(exclude={"password"}, exclude_defaults=True)

    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    if user_in.password:
        password = bytes(user_in.password, "utf-8")
        user.password = password

    db_session.commit()
    return user


def get_current_user(request: Request) -> AutheneUser:
    user_email = auth_provider.get_current_user(request)
    if not user_email:
        logger.exception(
            f"Unable to determine user email based on configured auth provider or no default auth user email defined."
        )
        raise InvalidCredentialException

    return get_or_create(
        db_session=request.state.db,
        user_in=UserRegister(email=user_email),
    )


CurrentUser = Annotated[AutheneUser, Depends(get_current_user)]


def get_current_role(request: Request, current_user: CurrentUser) -> UserRoles:
    """Attempts to get the current user depending on the configured authentication provider."""
    return current_user.role
