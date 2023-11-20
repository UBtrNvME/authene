from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from authene.auth.service import get_current_user
from authene.auth.views import auth_router, user_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

authenticated_api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

authenticated_api_router.include_router(user_router, prefix="/users", tags=["users"])


api_router.include_router(
    authenticated_api_router,
    dependencies=[Depends(get_current_user)],
)
