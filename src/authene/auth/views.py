from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from authene.auth.service import CurrentUser, create, get, get_all, get_by_email, update
from authene.exceptions import (
    InvalidConfigurationError,
    InvalidPasswordError,
    InvalidUsernameError,
)
from authene.models import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserPagination,
    UserRead,
    UserRegister,
    UserRegisterResponse,
    UserUpdate,
)
from authene_common.config import AUTHENE_AUTH_REGISTRATION_ENABLED
from authene_common.database import DbSession
from authene_common.models import PrimaryKey

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get(
    "",
    response_model=UserPagination,
)
def get_users(db_session: DbSession):
    """Gets all organization users."""

    items = get_all(db_session=db_session)

    return {
        "items": [
            {
                "id": u.id,
                "email": u.email,
                "role": u.role,
            }
            for u in items
        ],
        "itemsPerPage": len(items),
        "page": 1,
        "total": 1,
    }


@user_router.post(
    "",
    response_model=UserRead,
)
def create_user(
    user_in: UserCreate,
    db_session: DbSession,
    current_user: CurrentUser,
):
    """Creates a new user."""
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise ValidationError(
            [
                InvalidConfigurationError,
            ],
            model=UserCreate,
        )

    user = create(db_session=db_session, user_in=user_in)
    return user


@user_router.get("/{user_id}", response_model=UserRead)
def get_user(db_session: DbSession, user_id: PrimaryKey):
    """Get a user."""
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    return user


@user_router.put(
    "/{user_id}",
    response_model=UserRead,
)
def update_user(
    db_session: DbSession,
    user_id: PrimaryKey,
    user_in: UserUpdate,
    current_user: CurrentUser,
):
    """Update a user."""
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )
    return update(db_session=db_session, user=user, user_in=user_in)


@auth_router.get("/me", response_model=UserRead)
def get_me(
    *,
    db_session: DbSession,
    current_user: CurrentUser,
):
    return current_user


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_in: UserLogin,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user and user.check_password(user_in.password):
        projects = []
        for user_project in user.projects:
            projects.append(
                {
                    "project": user_project.project,
                    "default": user_project.default,
                    "role": user_project.role,
                }
            )
        return {"projects": projects, "token": user.token}

    raise ValidationError(
        [
            InvalidUsernameError,
            InvalidPasswordError,
        ],
        model=UserLogin,
    )


def register_user(
    user_in: UserRegister,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail=f"User with email '{user_in.email}' already exists."
        )

    user = create(db_session=db_session, user_in=user_in)
    return user


if AUTHENE_AUTH_REGISTRATION_ENABLED:
    register_user = auth_router.post("/register", response_model=UserRegisterResponse)(
        register_user
    )
